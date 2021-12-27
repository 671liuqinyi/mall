<template>
  <div id="user">
    <!-- 面包屑导航区 -->
    <el-breadcrumb el-breadseparator="/">
      <el-breadcrumb-item>首页</el-breadcrumb-item>
      <el-breadcrumb-item>用户管理</el-breadcrumb-item>
      <el-breadcrumb-item>用户列表</el-breadcrumb-item>
    </el-breadcrumb>
    <!-- 卡片区 -->
    <el-card>
      <el-row :gutter="15">
        <el-col :span="10">
          <!-- 搜索与添加区 -->
          <el-input placeholder="请输入搜索内容" v-model="queryInfo.query" clearable @clear='getUserList'>
            <el-button slot="append" icon="el-icon-search" @click="getUserList"></el-button>
          </el-input>
        </el-col>
        <el-col :span="5">
          <el-button type="primary" @click="addDialog = true">添加用户</el-button>
        </el-col>
      </el-row>

      <!-- 用户列表区 -->
      <el-table :data="userlist" border>
        <el-table-column type="index" label=""></el-table-column>
        <el-table-column label="用户名" prop="username"></el-table-column>
        <!-- <el-table-column label="邮箱" prop="email"></el-table-column> -->
        <!-- <el-table-column label="电话" prop="mobile"></el-table-column> -->
        <el-table-column label="角色" prop="role"> </el-table-column>
        <!-- <el-table-column label="状态" width="100px">
          <template slot-scope="scope" >
            <el-switch v-model="scope.row.mg_state" @change="userStateChange(scope.row)">
            </el-switch>
          </template>
        </el-table-column> -->
        <el-table-column label="操作" width="180px">
          <template slot-scope="scope">
            <!-- 修改用户 -->
            <el-button type="primary" icon="el-icon-edit" size="mini" @click="showEditDialog(scope.row.username)"></el-button>
            <!-- 删除用户 -->
            <el-button type="danger" icon="el-icon-delete" size="mini" @click="remove(scope.row.username)"></el-button>
            <!-- 分配角色 -->
            <el-tooltip effect="dark" content="分配角色" placement="top">
              <el-button type="warning" icon="el-icon-setting" size="mini" @click="setRole(scope.row.username)"></el-button>
            </el-tooltip>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页显示区 -->
      <el-pagination @current-change="handleCurrentChange" :page-size="PageSize" layout="total, prev, pager, next" :total="total">
      </el-pagination>
    </el-card>

    <!-- 添加用户的弹出框 -->
    <el-dialog title="添加用户" :visible.sync="addDialog" @close="addClose" width="50%">
      <el-form :model="addForm" :rules="addRuleForm" ref="addFormRef" label-width="70px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="addForm.username"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="addForm.password"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="addDialog = false">取 消</el-button>
        <el-button type="primary" @click="addUser">确 定</el-button>
      </span>
    </el-dialog>

    <!-- 编辑用户的弹出框 -->
    <el-dialog title="编辑用户" :visible.sync="editDialog" @close="addClose" width="50%" @click="editClose">
      <el-form :model="editFrom" :rules="addRuleForm" ref="addFormRef" label-width="70px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="editFrom.username" disabled></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="editFrom.password"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="editDialog = false">取 消</el-button>
        <el-button type="primary" @click="editUser">确 定</el-button>
      </span>
    </el-dialog>
    <!-- 分配角色弹出框 -->
    <el-dialog title="分配角色" :visible.sync="setRoleDialog" width="50%" @close="setRoleDialogClosed">
      <div>
        <p>当前的用户：{{userInfo.username}}</p>
        <p>当前的角色：{{userInfo.role}}</p>
        <p>分配新角色：
          <el-select v-model="selectedRoleid" placeholder="请选择">
            <el-option v-for="item in rolesList" :key="item.id" :label="item.role" :value="item.id">
            </el-option>
          </el-select>
        </p>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="setRoleDialog = false">取 消</el-button>
        <el-button type="primary" @click="saveRoleInfo">确 定</el-button>
      </span>
    </el-dialog>

  </div>
</template>

<script>
export default {
  data() {
    // 用户名的校验方法
    let validateName = (rule, value, callback) => {
      if (!value) {
        return callback(new Error('请输入用户名'))
      }
      // 用户名以字母开头,长度在5-16之间,允许字母数字下划线
      const userNameRule = /^[a-zA-Z][a-zA-Z0-9_]{4,15}$/
      if (userNameRule.test(value)) {
        //判断数据库中是否已经存在该用户名
        this.$axios
          .post('/api/adduser', {
            username: this.addForm.username,
            password: ''
          })
          .then(res => {
            // console.log(res.data.code)
            // “201”代表用户名存在，不可以注册
            if (res.data.code != '201') {
              this.$refs.addFormRef.validateField('checkPass')
              return callback()
            } else {
              return callback(new Error('用户名已存在'))
            }
          })
          .catch(err => {
            return Promise.reject(err)
          })
      } else {
        return callback(new Error('字母开头,长度5-16之间,允许字母数字下划线'))
      }
    }
    return {
      //获取用户列表参数对象
      queryInfo: {
        query: '',
        //当前的页数
        pagenum: 1,
        pagesize: 6
      },
      // 显示的用户信息对象
      userlist: [],
      // 查询到的全部用户信息对象
      alllist: [],
      editFrom: {},
      total: 0,
      PageSize: 5,
      currentPage: 1,
      addDialog: false,
      editDialog: false,
      addForm: {
        username: '',
        password: ''
      },
      addRuleForm: {
        username: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { validator: validateName, trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { pattern: /^[a-zA-Z][a-zA-Z0-9_]{5,16}$/, message: '字母开头,长度6-18之间,允许字母数字和下划线', trigger: 'blur' }
        ]
      },
      setRoleDialog: false,
      userInfo: {},
      rolesList: [
        { id: 1, role: '系统管理员' },
        { id: 2, role: '商家' },
        { id: 3, role: '普通员工' }
      ],
      selectedRoleid: ''
    }
  },
  created() {
    this.getUserList()
  },
  methods: {
    async getUserList() {
      let { data } = await this.$axios.get('/api/getuser', {
        params: { search: this.queryInfo.query }
      })
      // console.log(data)
      if (data.code == '200') {
        this.alllist = data.data
        this.userlist = data.data.slice(0, this.PageSize)
        this.total = data.total
      }
    },
    //监听页码值改变的事件
    handleCurrentChange(currentPage) {
      this.currentPage = currentPage
      let current = currentPage * this.PageSize
      let prev = current - this.PageSize
      this.userlist = this.alllist.slice(prev, current)
    },
    //添加对话框关闭重置事件
    addClose() {
      this.$refs.addFormRef.resetFields()
    },
    //添加用户事件
    addUser() {
      this.$refs.addFormRef.validate(async valid => {
        if (!valid) return
        let { data } = await this.$axios.post('/api/adduser', {
          username: this.addForm.username,
          password: this.addForm.password
        })
        if (data.code == '200') {
          this.$message.success('添加用户成功！')
          this.addDialog = false
          this.getUserList()
        } else {
          this.$message.error('添加用户失败！')
        }
      })
    },
    //编辑用户事件
    async showEditDialog(id) {
      let currentInfo = ''
      for (let i = 0; i < this.alllist.length; i++) {
        if (this.alllist[i].username == id) {
          currentInfo = this.alllist[i]
        }
      }
      this.editFrom = currentInfo
      this.editDialog = true
    },
    //编辑用户提交事件
    editUser() {
      this.$refs.addFormRef.validate(async valid => {
        if (!valid) return
        //发起修改用户信息的数据请求
        let { data } = await this.$axios.post('/api/editinfo', {
          username: this.editFrom.username,
          password: this.editFrom.password
        })
        if (data.code == '200') {
          this.editDialog = false
          this.getUserList()
          this.$message.success('用户信息编辑成功！')
        } else {
          this.$message.error('编辑失败！')
        }
      })
    },
    //编辑用户重置事件
    editClose() {
      this.$refs.editFrom.resetFields()
    },
    //删除用户
    async remove(id) {
      const res = await this.$confirm('是否删除该用户, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).catch(err => err)
      if (res == 'confirm') {
        let { data } = await this.$axios.post('/api/removeuser', {
          username: id
        })
        if (data.code == '200') {
          this.$message.success('删除用户成功！')
          this.getUserList()
        } else {
          this.$message.error('删除用户失败！')
        }
      }
    },
    //分配角色
    async setRole(userInfo) {
      let currentInfo = ''
      for (let i = 0; i < this.alllist.length; i++) {
        if (this.alllist[i].username == userInfo) {
          currentInfo = this.alllist[i]
        }
      }
      this.userInfo = currentInfo
      this.setRoleDialog = true
    },
    //点击确定按钮分配角色
    async saveRoleInfo() {
      if (!this.selectedRoleid) {
        return this.$message.error('请选择要分配的角色！')
      }
      let { data } = await this.$axios.post('/api/changerole', {
        username: this.userInfo.username,
        role: this.selectedRoleid
      })
      if (data.code == '200') {
        this.$message.success('更新权限成功！')
        this.getUserList()
      } else {
        this.$message.error('更新权限失败！')
      }
      this.setRoleDialog = false
    },
    // 分配角色对话框关闭事件
    setRoleDialogClosed() {
      this.selectedRoleid = ''
      this.userInfo = {}
    }
  }
}
</script>

<style>
</style>