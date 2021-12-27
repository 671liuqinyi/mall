<template>
  <div>
    <!-- 面包屑导航区 -->
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item>首页</el-breadcrumb-item>
      <el-breadcrumb-item>商品管理</el-breadcrumb-item>
      <el-breadcrumb-item>商品列表</el-breadcrumb-item>
    </el-breadcrumb>
    <!-- 卡片视图 -->
    <el-card>
      <el-row :gutter="20">
        <el-col :span="6">
          <el-input placeholder="请输入内容" v-model="queryInfo.query" clearable @clear="getGoodsList">
            <el-button slot="append" icon="el-icon-search" @click="getGoodsList"></el-button>
          </el-input>
        </el-col>
        <el-col :span="4">
          <el-button type="primary" @click="addDialog = true">添加商品</el-button>
        </el-col>
      </el-row>
      <!-- 表格数据 -->
      <el-table :data="goodsList" border stripe>
        <el-table-column type="index"></el-table-column>
        <el-table-column label="商品名称" prop="goods_name"></el-table-column>
        <el-table-column label="原价(元)" prop="goods_price" width="80px"></el-table-column>
        <el-table-column label="特价(元)" prop="goods_sale" width="80px"></el-table-column>
        <el-table-column label="剩余库存" prop="goods_number" width="80px"></el-table-column>
        <el-table-column label="创建时间" prop="add_time" width="160px">
          <template slot-scope="scope">{{scope.row.add_time}}</template>
        </el-table-column>
        <el-table-column label="操作" width="130px">
          <template slot-scope="scope">
            <el-button type="primary" icon="el-icon-edit" size="mini" @click="showEditDialog(scope.row.goods_id)"></el-button>
            <el-button type="danger" icon="el-icon-delete" size="mini" @click="removeById(scope.row.goods_id)"></el-button>
          </template>
        </el-table-column>
      </el-table>
      <!-- 分页区域 -->
      <el-pagination @current-change="handleCurrentChange" :page-size="PageSize" layout="total, prev, pager, next" :total="total" background></el-pagination>
    </el-card>
    <!-- 添加商品的弹出框 -->
    <el-dialog title="添加商品" :visible.sync="addDialog" @close="addClose" width="50%">
      <el-form :model="addForm" :rules="addRuleForm" ref="addFormRef" label-width="70px">
        <el-form-item label="商品名" prop="goods_name">
          <el-input v-model="addForm.goods_name"></el-input>
        </el-form-item>
        <el-form-item label="原价" prop="goods_price">
          <el-input v-model="addForm.goods_price"></el-input>
        </el-form-item>
        <el-form-item label="特价" prop="goods_sale">
          <el-input v-model="addForm.goods_sale"></el-input>
        </el-form-item>
        <el-form-item label="数量" prop="goods_number">
          <el-input v-model="addForm.goods_number"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="addDialog = false">取 消</el-button>
        <el-button type="primary" @click="addGoods">确 定</el-button>
      </span>
    </el-dialog>
    <!-- 编辑商品的弹出框 -->
    <el-dialog title="修改商品信息" :visible.sync="editDialog" @close="addClose" width="50%" @click="editClose">
      <el-form :model="editFrom" :rules="addRuleForm" ref="addFormRef" label-width="70px">
        <el-form-item label="商品名" prop="goods_name">
          <el-input v-model="editFrom.goods_name"></el-input>
        </el-form-item>
        <el-form-item label="原价" prop="goods_price">
          <el-input v-model="editFrom.goods_price"></el-input>
        </el-form-item>
        <el-form-item label="特价" prop="goods_sale">
          <el-input v-model="editFrom.goods_sale"></el-input>
        </el-form-item>
        <el-form-item label="数量" prop="goods_number">
          <el-input v-model="editFrom.goods_number"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="editDialog = false">取 消</el-button>
        <el-button type="primary" @click="editGoods">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  data() {
    return {
      queryInfo: {
        query: '',
        pagenum: 1,
        pagesize: 10
      },
      // 显示商品列表
      goodsList: [],
      // 全部商品列表
      alllist: [],
      // 商品总数
      total: 0,
      // 一页大小
      PageSize: 8,
      addDialog: false,
      editDialog: false,
      addForm: {},
      editFrom: {},
      addRuleForm: {
        goods_name: [{ required: true, message: '请输入商品名称', trigger: 'blur' }],
        goods_price: [
          { required: true, message: '请输入商品原价', trigger: 'blur' },
          { pattern: /^[0]$|^[1-9]{1}[0-9]{0,9}$/, message: '价格为数字,长度1-10位', trigger: 'blur' }
        ],
        goods_sale: [
          { required: true, message: '请输入商品特价', trigger: 'blur' },
          { pattern: /^[0]$|^[1-9]{1}[0-9]{0,9}$/, message: '价格为数字,长度1-10位', trigger: 'blur' }
        ],
        goods_number: [
          { required: true, message: '请输入商品数量', trigger: 'blur' },
          { pattern: /^[0]$|^[1-9]{1}[0-9]{0,9}$/, message: '商品数量为数字,长度1-10位', trigger: 'blur' }
        ]
      }
    }
  },
  created() {
    this.getGoodsList()
  },
  methods: {
    // 根据分页获取对应的商品列表
    async getGoodsList() {
      let { data } = await this.$axios.get('/api/getgoods', {
        params: { search: this.queryInfo.query }
      })
      // console.log(data)
      if (data.code == '200') {
        this.alllist = data.data
        this.goodsList = data.data.slice(0, this.PageSize)
        this.total = data.total
      }
    },
    handleCurrentChange(currentPage) {
      this.currentPage = currentPage
      let current = currentPage * this.PageSize
      let prev = current - this.PageSize
      this.goodsList = this.alllist.slice(prev, current)
    },

    //添加对话框关闭重置事件
    addClose() {
      this.$refs.addFormRef.resetFields()
    },
    //添加商品事件
    addGoods() {
      this.$refs.addFormRef.validate(async valid => {
        if (!valid) return
        let { data } = await this.$axios.post('/api/addgoods', {
          goods_name: this.addForm.goods_name,
          goods_price: this.addForm.goods_price,
          goods_sale: this.addForm.goods_sale,
          goods_number: this.addForm.goods_number
        })
        if (data.code == '200') {
          this.$message.success('添加商品成功！')
          this.addDialog = false
          this.getGoodsList()
        } else {
          this.$message.error('添加商品失败！')
        }
      })
    },
    //编辑商品事件
    async showEditDialog(id) {
      let currentInfo = ''
      for (let i = 0; i < this.alllist.length; i++) {
        if (this.alllist[i].goods_id == id) {
          currentInfo = this.alllist[i]
        }
      }
      this.editFrom = currentInfo
      this.editDialog = true
    },
    //编辑商品提交事件
    editGoods() {
      this.$refs.addFormRef.validate(async valid => {
        if (!valid) return
        //发起修改用户信息的数据请求
        let { data } = await this.$axios.post('/api/editgoods', {
          goods_id: this.editFrom.goods_id,
          goods_name: this.editFrom.goods_name,
          goods_price: this.editFrom.goods_price,
          goods_sale: this.editFrom.goods_sale,
          goods_number: this.editFrom.goods_number
        })
        if (data.code == '200') {
          this.editDialog = false
          this.getGoodsList()
          this.$message.success('商品信息编辑成功！')
        } else {
          this.$message.error('商品信息编辑失败！')
        }
      })
    },
    //编辑用户重置事件
    editClose() {
      this.$refs.editFrom.resetFields()
    },

    // 通过Id删除商品
    async removeById(id) {
      const confirmResult = await this.$confirm('此操作将永久删除该商品, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).catch(err => err)
      if (confirmResult !== 'confirm') {
        return
      }
      let { data } = await this.$axios.post('/api/deletegoods', {
        goods_id: id
      })
      console.log(data)
      if (data.code == '200') {
        this.$message.success('删除商品成功！')
        this.getGoodsList()
      } else {
        this.$message.error('删除商品失败！')
      }
    }
  }
}
</script>

<style lang="less" scoped>
</style>