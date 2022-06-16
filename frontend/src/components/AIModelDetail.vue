<template>
  <div id="flex-container">
    <span style="font-weight: bold; font-size: larger">
      模型：{{name}}
    </span>
    <el-divider/>
    <div>
       <span>
        训练日志
      </span>
    </div>
    <br/>
    <div>
      <pre class="log-display" :class="logClass">
        {{this.train_log}}
      </pre>
    </div>
    <br/>
    <div>
      <span>
        评估日志
      </span>
    </div>
    <br/>
    <div>
      <pre class="log-display" :class="logClass">
        {{this.evaluate_log}}
      </pre>
    </div>
  </div>
</template>

<script>
// import {VueEditor} from "vue2-editor"
export default {
  name: "AIModelDetail",
  // components:{
  //   VueEditor
  // },
  data(){
    return {
      train_log: '',
      evaluate_log: '',
      name: '',
      logClass: {}
    }
  },
  created() {
    this.$http.get(`/models/${this.$route.params.id}`).then((response)=>{
      this.train_log = response.data.train_log
      this.evaluate_log = response.data.evaluate_log
      this.name = response.data.name
    })
  },
  mounted() {
    this.logClass = {
      width: document.getElementById('flex-container').clientWidth * 0.9 + 'px',
    }
  }
}
</script>
<style scoped lang="less">
.flex-container{
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
}
.log-display{
  overflow-x: scroll;
  overflow-y: scroll;
  border: 1px solid #eee;
  height: 400px;
  box-shadow: 0 1px 2px 0 rgb(0 0 0 / 15%)
}
</style>