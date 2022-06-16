<template>
  <div class="operation-button-wrapper">
    <el-button-group>
      <el-tooltip content="点击后将自动保存">
        <el-button icon="el-icon-arrow-left" :disabled="isBackDisabled" @click="setNextOrBack(false)"> 上一张图片</el-button>
      </el-tooltip>
      <el-tooltip content="点击后将自动保存">
        <el-button icon="el-icon-arrow-right" :disabled="isNextDisabled" @click="setNextOrBack(true)"> 下一张图片</el-button>
      </el-tooltip>
    </el-button-group>
    <el-button type="primary" icon="el-icon-document-checked" @click="save">保存当前标注</el-button>
  </div>
</template>

<script>
export default {
  name: "AnnotateWorkshopTitle",
  data(){
    return {
      activeIndex: 0,
    }
  },
  computed:{
    isNextDisabled(){
      return this.$store.state.annotate.activeIndex === (this.$store.getters["annotate/thumbnailImageListLength"] - 1)
    },
    isBackDisabled(){
      return this.$store.state.annotate.activeIndex === 0
    }
  },
  methods:{
    save(){
      this.$store.dispatch('annotate/checkAndSave').then((valid) =>{
          if(!valid){
            this.$message({
              message: '所有标注框必须设置标签',
              type: 'warning'
            })
          }
      })
    },

    setNextOrBack(nextFlag){
      this.$store.dispatch("annotate/checkAndSave").then((valid) =>{
        if(valid){
          // 保存成功才能跳转
          if(nextFlag){
            this.$store.commit("annotate/setActiveIndex", this.$store.state.annotate.activeIndex + 1)
          }else{
            this.$store.commit("annotate/setActiveIndex", this.$store.state.annotate.activeIndex - 1)
          }
        }else{
          this.$message({
            message: '所有标注框必须设置标签',
            type: 'warning'
          })
        }
      })
    }
  },
}
</script>

<style scoped>
.operation-button-wrapper{
  display: flex;
  justify-content: space-between;
}
</style>