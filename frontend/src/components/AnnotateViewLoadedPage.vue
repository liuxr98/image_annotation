<template>
  <div class="workshop-wrapper">
    <div class="workshop">
      <div class="left-panel" >
        <el-tabs @tab-click="handleClick" :active-name="activeTab">
          <el-tab-pane label="未标注" name="Unlabeled"/>
          <el-tab-pane label="已标注" name="Labeled"/>
          <el-tab-pane label="所有" name="All"/>
        </el-tabs>
        <el-button type="primary" class="tabs-button" size="small" v-if="reviewButtonVisible" @click="handleReview">
          全部验收通过
        </el-button>
        <annotate-workshop-title class="workshop-title"/>
        <annotate-image-canvas class="image-canvas"/>
        <annotate-thumbnail-slider class="thumbnail-slider"/>
      </div>
      <div class="right-panel">
        <label-picker/>
      </div>
    </div>
  </div>
</template>

<script>
import AnnotateImageCanvas from "@/components/AnnotateImageCanvas";
import AnnotateThumbnailSlider from "@/components/AnnotateThumbnailSlider";
import AnnotateWorkshopTitle from "@/components/AnnotateWorkshopTitle";
import LabelPicker from "@/components/LabelPicker";
import {taskTypes} from "@/util/enum";

export default {
  name: "AnnotateViewLoadedPage",
  components:{
    AnnotateImageCanvas,
    AnnotateThumbnailSlider,
    AnnotateWorkshopTitle,
    LabelPicker
  },
  computed:{
    activeTab(){
      return this.$store.state.annotate.category
    },
    reviewButtonVisible(){
      return this.$store.state.annotate.taskType === taskTypes.Review
    }
  },
  methods:{
    handleClick(tab){
      this.$store.commit('annotate/setCategory', tab.name)
    },
    handleReview(){
      this.$store.dispatch('annotate/reviewTeamTaskInAnnotate')
      this.$store.commit('annotate/setDatasetID', '') // 将datasetID置空，从而显示task页面
    }
  },
  created() {
    this.$store.dispatch("annotate/initAnnotate")
  }
}
</script>

<style scoped>
.workshop-wrapper{
  display: flex;
  flex-direction: column;
}
.workshop{
  display: flex;
  position: relative;
}
.tabs-button{
  position: absolute;
  right: 5px;
  top: 2px
}
.left-panel{
  width: 0;
  flex: 1;
  display: flex;
  flex-direction: column;
  position: relative;
  margin-right: 35px;
}
.right-panel{
  width: 420px;
  flex-basis: 420px;
  max-width: 420px;
  min-width: 420px;
  background-color: #f7f7f7;
  flex-shrink: 0;
  flex-grow: 0;
}
.image-canvas{
  border: 1px solid #eee;
  box-shadow: 0 1px 2px 0 rgb(0 0 0 / 15%)
}
.thumbnail-slider{
  margin-top: 20px;
}
.workshop-title {
  margin-bottom: 10px;
}

</style>