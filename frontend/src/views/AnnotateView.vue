<template>
  <AnnotateViewLoadedPage v-if="isLoaded"/>
  <div v-else class="center-content">
    <div class="select-wrapper">
      <el-empty description="请选择需要标注的数据集">
        <div style="margin-bottom: 20px">
        <el-alert
            type="info"
            show-icon
            title="处于团队标注或智能标注的数据集将不可选"
            :closable="false"
        />
        </div>
        <el-select v-model="datasetID" placeholder="请选择数据集" @change="setDatasetID">
          <el-option
              v-for="dataset in datasets"
              :key="dataset.id"
              :label="dataset.name"
              :value="dataset.id"
              :disabled="dataset.status !== 'None'"
          />
        </el-select>
      </el-empty>
    </div>
  </div>
</template>

<script>
import AnnotateViewLoadedPage from "@/components/AnnotateViewLoadedPage";
import {mapState} from "vuex";
import {taskTypes} from "@/util/enum";

export default {
  name: "AnnotateView",
  components:{
    AnnotateViewLoadedPage
  },
  data(){
    return {
      datasetID: null,
    }
  },
  computed:{
    isLoaded(){
      if(this.datasetID){
        return true
      }
      return false
    },
    ...mapState('dataset', ['datasets'])
  },
  methods:{
    setDatasetID(val){
      this.$store.commit('annotate/setTaskType', taskTypes.Annotate)
      this.$store.commit("annotate/setDatasetID",val)
    }
  },
  created() {
    this.$store.dispatch('dataset/getDatasets')
  }
}
</script>

<style scoped lang="css">
.center-content{
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}
.select-wrapper{
  position:relative;
  bottom: 25%;
}
</style>