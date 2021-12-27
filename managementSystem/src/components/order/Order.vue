<template>
  <div>
    <!-- 面包屑导航区 -->
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item>首页</el-breadcrumb-item>
      <el-breadcrumb-item>订单管理</el-breadcrumb-item>
      <el-breadcrumb-item>订单列表</el-breadcrumb-item>
    </el-breadcrumb>
    <!-- 卡片视图 -->
    <el-card>
      <el-row :gutter="20">
        <el-col :span="6">
          <el-input placeholder="请输入内容" v-model="queryInfo.query" clearable @clear="getGoodsList">
            <el-button slot="append" icon="el-icon-search" @click="getGoodsList"></el-button>
          </el-input>
        </el-col>
      </el-row>
      <!-- 表格数据 -->
      <el-table :data="goodsList" border stripe>
        <el-table-column type="index"></el-table-column>
        <el-table-column label="订单编号" prop="order_no"></el-table-column>
        <el-table-column label="订单价格(元)" prop="total_price"></el-table-column>
        <el-table-column label="支付状态" prop="pay_status">
          <template slot-scope="scope">
            <el-tag type="success" v-if="scope.row.pay_status == '1'">已付款</el-tag>
            <el-tag type="danger" v-else>未付款</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="购物者" prop="user_name"></el-table-column>
        <el-table-column label="创建时间" prop="create_time">
          <template slot-scope="scope">{{scope.row.create_time}}</template>
        </el-table-column>
        <el-table-column label="操作" >
          <template slot-scope="scope">
            <el-button type="primary" icon="el-icon-edit" size="mini" @click="showEditDialog(scope.row.order_no)"></el-button>
            <el-button type="danger" icon="el-icon-delete" size="mini" @click="removeById(scope.row.order_no)"></el-button>
          </template>
        </el-table-column>
      </el-table>
      <!-- 分页区域 -->
      <el-pagination @current-change="handleCurrentChange" :page-size="PageSize" layout="total, prev, pager, next" :total="total" background></el-pagination>
    </el-card>
    <!-- 编辑商品的弹出框 -->
    <el-dialog title="修改订单信息" :visible.sync="editDialog" @close="editClose" width="50%" @click="editClose">
      <el-form :model="editFrom" :rules="addRuleForm" ref="addFormRef" label-width="70px">
        <el-form-item label="订单编号" prop="order_no">
          <el-input v-model="editFrom.order_no" disabled></el-input>
        </el-form-item>
        <el-form-item label="购物者" prop="user_name">
          <el-input v-model="editFrom.user_name" disabled></el-input>
        </el-form-item>
        <el-form-item label="价格" prop="total_price">
          <el-input v-model="editFrom.total_price"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="editDialog = false">取 消</el-button>
        <el-button type="primary" @click="editOrders">确 定</el-button>
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
      editDialog: false,
      editFrom: {},
      addRuleForm: {
        total_price: [
          { required: true, message: '请输入商品原价', trigger: 'blur' },
          { pattern: /^[0]$|^[1-9]{1}[0-9]{0,9}$/, message: '价格为数字,长度1-10位', trigger: 'blur' }
        ]
      }
    }
  },
  created() {
    this.getGoodsList()
  },
  methods: {
    // 根据分页获取对应的订单列表
    async getGoodsList() {
      let { data } = await this.$axios.get('/api/findorder', {
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

    //编辑订单事件
    async showEditDialog(id) {
      let currentInfo = ''
      for (let i = 0; i < this.alllist.length; i++) {
        if (this.alllist[i].order_no == id) {
          currentInfo = this.alllist[i]
        }
      }
      this.editFrom = currentInfo
      this.editDialog = true
    },
    //编辑订单提交事件
    editOrders() {
      this.$refs.addFormRef.validate(async valid => {
        if (!valid) return
        //发起修改订单信息的数据请求
        let { data } = await this.$axios.post('/api/editorders', {
          order_no: this.editFrom.order_no,
          total_price: this.editFrom.total_price
        })
        if (data.code == '200') {
          this.editDialog = false
          this.getGoodsList()
          this.$message.success('订单信息编辑成功！')
        } else {
          this.$message.error('订单信息编辑失败！')
        }
      })
    },
    //编辑订单重置事件
    editClose() {
      this.$refs.addFormRef.resetFields()
    },
    // 通过Id删除订单
    async removeById(id) {
      const confirmResult = await this.$confirm('此操作将永久删除该商品, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).catch(err => err)
      if (confirmResult !== 'confirm') {
        return
      }
      let { data } = await this.$axios.post('/api/deleteorders', {
        order_id: id
      })
      // console.log(data)
      if (data.code == '200') {
        this.$message.success('删除订单成功！')
        this.getGoodsList()
      } else {
        this.$message.error('删除订单失败！')
      }
    }
  }
}
</script>

<style lang="less" scoped>
</style>