<template>
  <div class="login">
    <div class="login_box">
      <!-- logo区域 -->
      <div class="avatar_box">
        <img :src="imgSrc" alt="">
      </div>
      <!-- 表单区域 -->
      <el-form ref="loginRef" :model="loginForm" class="card" :rules="loginRules">
        <!-- 用户名 -->
        <el-form-item prop="username">
          <el-input v-model="loginForm.username" placeholder="请输入用户名" prefix-icon="el-icon-user-solid"></el-input>
        </el-form-item>
        <!-- 密码 -->
        <el-form-item prop="password">
          <el-input v-model="loginForm.password" placeholder="请输入密码" prefix-icon="el-icon-lock" type="password"></el-input>
        </el-form-item>
        <!-- 按钮区域 -->
        <el-form-item class="btns">
          <el-button type="primary" @click="login">登录</el-button>
          <el-button type="info" @click="resetForm">重置</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      loginForm: {
        username: 'admin',
        password: 'admin12'
      },
      imgSrc: require('../assets/images/logo.png'),
      //验证规则
      loginRules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
          { pattern: /^[a-zA-Z][a-zA-Z0-9_]{4,15}$/, message: '字母开头,长度5-16之间,允许字母数字下划线', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { pattern: /^[a-zA-Z][a-zA-Z0-9_]{5,16}$/, message: '字母开头,长度6-18之间,允许字母数字和下划线', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    //登录功能按钮
    login() {
      this.$refs.loginRef.validate(async valid => {
        if (!valid) return
        let { data } = await this.$axios.post('/api/adminlogin', this.loginForm)
        // console.log(data)
        if (data.code == '200') {
          this.$message.success('登录成功!')
          sessionStorage.setItem('admin', JSON.stringify(data.data))
          this.$router.push('/home')
        } else {
          this.$message.error('用户名或密码错误!')
        }
      })
    },
    //重置功能按钮
    resetForm() {
      this.loginForm.username = ''
      this.loginForm.password = ''
    }
  }
}
</script>

<style  lang="less" scoped>
.login {
  // background-color: #2b4b6b;
  background: url(../assets/images/bg3.jpg);
  background-repeat: no-repeat;
  background-size: 100% 100%;
  height: 100%;
}
.login_box {
  width: 450px;
  height: 300px;
  background-color: whitesmoke;
  border-radius: 10px;
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
}
.avatar_box {
  width: 130px;
  height: 130px;
  border: 1px solid #eee;
  border-radius: 50%;
  padding: 10px;
  box-shadow: 0 0 10px #ddd;
  position: absolute;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: #fff;
  img {
    width: 100%;
    height: 100%;
    border-radius: 50%;
    background-color: #eee;
  }
}
.card {
  position: absolute;
  bottom: 0;
  width: 100%;
  padding: 0 20px;
  box-sizing: border-box;
}
.btns {
  display: flex;
  justify-content: flex-end;
}
</style>