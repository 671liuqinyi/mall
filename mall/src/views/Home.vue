<!--
 * @Description: 首页组件
 * @Author: hai-27
 * @Date: 2020-02-07 16:23:00
 * @LastEditors: hai-27
 * @LastEditTime: 2020-02-27 13:36:12
 -->
<template>
  <div class="home" id="home" name="home">
    <!-- 轮播图 -->
    <div class="block">
      <el-carousel height="460px">
        <el-carousel-item v-for="item in carousel" :key="item.carousel_id">
          <img style="height:460px;" src="../assets/tempimgs/car.jpg" alt="item.describes" />
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
              <!-- <MyMenu :val="2" @fromChild="getChildMsg">
                <span slot="1">热门</span>
                <span slot="2">电视影音</span>
              </MyMenu> -->
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
      carousel: [{}, {}, {}, {}], // 轮播图数据
      phoneList: [], // 手机商品列表
      dailygoodsList: [], // 日常用品列表
      /* applianceActive: 1, // 家电当前选中的商品分类
      accessoryActive: 1 // 配件当前选中的商品分类 */
    }
  },
/*   watch: {
    // 家电当前选中的商品分类，响应不同的商品数据
    applianceActive: function (val) {
      // 页面初始化的时候把applianceHotList(热门家电商品列表)直接赋值给applianceList(家电商品列表)
      // 所以在切换商品列表时判断applianceHotList是否为空,为空则是第一次切换,把applianceList赋值给applianceHotList
      if (this.applianceHotList == '') {
        this.applianceHotList = this.applianceList
      }
      if (val == 1) {
        // 1为热门商品
        this.applianceList = this.applianceHotList
        return
      }
      if (val == 2) {
        // 2为电视商品
        this.applianceList = this.miTvList
        return
      }
    },
    accessoryActive: function (val) {
      // 页面初始化的时候把accessoryHotList(热门配件商品列表)直接赋值给accessoryList(配件商品列表)
      // 所以在切换商品列表时判断accessoryHotList是否为空,为空则是第一次切换,把accessoryList赋值给accessoryHotList
      if (this.accessoryHotList == '') {
        this.accessoryHotList = this.accessoryList
      }
      if (val == 1) {
        // 1为热门商品
        this.accessoryList = this.accessoryHotList
        return
      }
      if (val == 2) {
        // 2为保护套商品
        this.accessoryList = this.protectingShellList
        return
      }
      if (val == 3) {
        //3 为充电器商品
        this.accessoryList = this.chargerList
        return
      }
    }
  }, */
  created() {
    // 获取轮播图数据
    /* this.$axios
      .post("/api/resources/carousel", {})
      .then(res => {
        this.carousel = res.data.carousel;
      })
      .catch(err => {
        return Promise.reject(err);
      }); */
    // 获取各类商品数据
    this.getPromo('phone')
    this.getPromo('dailygoods')
    /* this.getPromo("电视机", "miTvList");
    this.getPromo("保护套", "protectingShellList");
    this.getPromo("充电器", "chargerList");
    this.getPromo(
      ["电视机", "空调", "洗衣机"],
      "applianceList",
      "/api/product/getHotProduct"
    );
    this.getPromo(
      ["保护套", "保护膜", "充电器", "充电宝"],
      "accessoryList",
      "/api/product/getHotProduct"
    ); */
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
/*     // 获取家电模块子组件传过来的数据
    getChildMsg(val) {
      this.applianceActive = val
    },
    // 获取配件模块子组件传过来的数据
    getChildMsg2(val) {
      this.accessoryActive = val
    }, */
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
      /* .then(res => {
          this[val] = res.data.Product
        })
        .catch(err => {
          return Promise.reject(err)
        }) */
    }
  }
}
</script>
<style scoped>
@import '../assets/css/index.css';
</style>