<template>
  <div>
    <!-- 面包屑导航区 -->
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item to="/welcome">首页</el-breadcrumb-item>
    </el-breadcrumb>
    <!-- 卡片视图 -->
    <el-card>
      <!-- 2.为Echarts准备一个Dom -->
      <div id="main" style="width: 1084px;height:470px;"></div>
    </el-card>
  </div>
</template>

<script>
// 1.导入echarts
import * as echarts from 'echarts'
import _ from 'lodash'

export default {
  data() {
    return {
      // 需要合并的数据
      options: {},
      // 显示数据
      allData: [],
      // 本星期日期
      Week: [],
      yAxisData1: [0, 0, 0, 0, 0, 0, 0],
      yAxisData2: [0, 0, 0, 0, 0, 0, 0]
    }
  },
  mounted() {
    this.getData()
  },
  // 此时,页面上的元素,已经被渲染完毕了
  methods: {
    async getData() {
      let { data } = await this.$axios.post('/api/salesdata', {
        search: 'week'
      })
      console.log(data)
      // console.log((new Date()).toLocaleDateString())
      if (data.code == '200') {
        this.allData = data.data
        this.Week = data.Week.reverse()
        // 计算y轴数据
        for (let i = 0; i < this.allData.length; i++) {
          for (let j = 0; j < 7; j++) {
            if (this.allData[i].create_time == this.Week[j]) {
              this.yAxisData1[j] += this.allData[i].total_price
              this.yAxisData2[j] += this.allData[i].count
              break
            }
          }
        }
        console.log(this.yAxisData1)
        console.log(this.yAxisData2)
        // 3.基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('main'))
        // 4.准备数据项和配置项
        // 指定图表的配置项和数据
        var option = {
          title: {
            text: '本周销售数据'
          },
          tooltip: {},
          toolbox: {
            feature: {
              saveAsImage: {},
              dataView: {},
              restore: {},
              dataZoom: {},
              magicType: {
                type: ['line', 'bar']
              }
            }
          },
          legend: {
            data: ['销量', '销售额']
          },
          xAxis: {
            type: 'category',
            data: this.Week
          },
          yAxis: {
            type: 'value'
          },
          series: [
            {
              name: '销量',
              type: 'line',
              data: this.yAxisData2,
              // data: [5, 20, 36, 10, 10, 20, 11],
              markPoint: {
                data: [
                  { type: 'max', name: '最大值' },
                  { type: 'min', name: '最小值' }
                ]
              },
              markLine: {
                data: [{ type: 'average', name: '平均值' }]
              },
              label: {
                show: true
              }
            },
            {
              name: '销售额',
              type: 'line',
              data: this.yAxisData1,
              // data: [3, 27, 16, 40, 80, 10, 17],
              markPoint: {
                data: [
                  { type: 'max', name: '最大值' },
                  { type: 'min', name: '最小值' }
                ]
              },
              markLine: {
                data: [{ type: 'average', name: '平均值' }]
              },
              label: {
                show: true
              }
            }
          ]
        }
        // 5.展示数据
        myChart.setOption(option)
      }
    }
  }
}
</script>

<style lang="less" scoped>
#main,
#main2 {
  float: left;
}
</style>