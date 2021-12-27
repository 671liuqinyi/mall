<template>
  <div class="home" id="home" name="home">
    <!-- 轮播图 -->
    <div class="block">
      <el-carousel height="460px">
        <el-carousel-item>
          <img style="height:460px;" src="../assets/tempimgs/carousel1.jpg" :alt="item" />
        </el-carousel-item>
        <el-carousel-item>
          <img style="height:460px;" src="../assets/tempimgs/carousel2.webp" :alt="item" />
        </el-carousel-item>
        <el-carousel-item>
          <img style="height:460px;" src="../assets/tempimgs/carousel3.jpg" :alt="item" />
        </el-carousel-item>
        <el-carousel-item>
          <img style="height:460px;" src="../assets/tempimgs/carousel4.webp" :alt="item" />
        </el-carousel-item>
      </el-carousel>
    </div>
    <!-- 轮播图END -->
    <div class="main-box">
      <div class="main">
        <!-- 手机商品展示区域 -->
        <div class="phone">
          <div class="box-hd">
            <div class="title">手机</div>
          </div>
          <div class="box-bd">
            <div class="promo-list">
              <router-link to>
                <img src="../assets/tempimgs/sidephone.png" />
              </router-link>
            </div>
            <div class="list">
              <MyList :list="phoneList" :isMore="true" :classid="[1]"></MyList>
            </div>
          </div>
        </div>
        <!-- 手机商品展示区域END -->

        <!-- 日常用品展示区域 -->
        <div class="appliance" id="promo-menu">
          <div class="box-hd">
            <div class="title">日常用品</div>
            <div class="more" id="more">

            </div>
          </div>
          <div class="box-bd">
            <div class="promo-list">
              <ul>
                <li>
                  <img src="../assets/tempimgs/dailygoods1.jpg" />
                </li>
                <li>
                  <img src="../assets/tempimgs/dailygoods2.jpg" />
                </li>
              </ul>
            </div>
            <div class="list">
              <MyList :list="dailygoodsList" :isMore="true" :classid="[2]"></MyList>
            </div>
          </div>
        </div>
        <!-- 日常用品展示区域END -->

      </div>
    </div>
  </div>
</template>
<script>
export default {
  data() {
    return {
      carousel: [], // 轮播图数据
      phoneList: [], // 手机商品列表
      dailygoodsList: [] // 日常用品列表
    }
  },
  created() {
    // 获取各类商品数据
    this.getPromo('phone')
    this.getPromo('dailygoods')
  },
  methods: {
    // 打乱数组
    shuffle(arr) {
      var l = arr.length
      var index, temp
      while (l > 0) {
        index = Math.floor(Math.random() * l)
        temp = arr[l - 1]
        arr[l - 1] = arr[index]
        arr[index] = temp
        l--
      }
      return arr
    },

    // 获取各类商品数据方法封装
    async getPromo(type) {
      let { data } = await this.$axios.get('/api/getproduct', {
        params: { type: type }
      })
      // 打乱并截取
      data.data = this.shuffle(data.data).slice(0, 7)
      if (data.code == '200') {
        if (type == 'phone') {
          this.phoneList = data.data
          // console.log(this.phoneList)
        } else if (type == 'dailygoods') {
          this.dailygoodsList = data.data
        }
      }
    }
  }
}
</script>
<style scoped>
@import '../assets/css/index.css';
</style>