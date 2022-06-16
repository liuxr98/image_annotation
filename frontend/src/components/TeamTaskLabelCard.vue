<template>
  <el-card shadow="never" class="label-card">
      <div v-if="showAddLabel">
        <BaseLabelColorInput
            @cancel="showAddLabel=false"
            @change="handleAddLabelCommit"
        />
      </div>
      <div v-else>
        <el-button
            type="primary"
            @click="showAddLabel=true"
            icon="el-icon-plus"
            style="width: 100%"
            plain
        >
          添加标签
        </el-button>
      </div>
      <div class="label-list-wrapper">
          <base-label-color-click-to-edit
              v-for="label in labels"
              :key="label.id"
              :label="label"
              class="label-item"
              @delete="deleteLabel(label.id)"
              :validator="editCommitValidator"
          />
    </div>
  </el-card>
</template>

<script>
import BaseLabelColorClickToEdit from "@/components/BaseLabelColorClickToEdit";
import BaseLabelColorInput from "@/components/BaseLabelColorInput";
import Vue from "vue";
export default {
  name: "TeamTaskLabelCard",
  components: {BaseLabelColorInput, BaseLabelColorClickToEdit},
  props:{
    datasetId:{
      required: true
    },
    labelsBind: Array
  },
  model:{
    prop: 'labelsBind',
    event: 'change'
  },
  watch: {
    datasetId() {
      this.loadLabels()
    }
  },
  data(){
    return{
      showAddLabel: false,
      labels: this.labelsBind
    }
  },
  methods:{
    deleteLabel(id){
      Vue.axios.delete(`/datasets/labels/${id}`).then(()=>{
        this.loadLabels()
      })
    },

    handleAddLabelCommit(value){
      if(!value.name){
        this.$message.error('标签名不能为空')
        return
      }
      if(!value.color){
        this.$message.error('颜色不能为空')
        return
      }
      // 检查添加的标签是否与数据集已有的标签重复
      for (let label of this.labels) {
        if (label.name === value.name) {
          this.$message.error('标签重复，请修改添加的标签名称')
          return
        }
      }
      // 通过check,则提交
      this.$http.post(`/datasets/${this.datasetId}/labels`,{
        labelGroupImportFlag: false,
        label: value
      }).then(()=>{
        this.loadLabels()
      }).catch(()=>{
        this.$message.error('导入失败')
      })
      this.showAddLabel = false
    },

    editCommitValidator(oldLabel, newLabel){
      // 如果修改前后的值相同，则直接返回true
      if(oldLabel.name === newLabel.name && oldLabel.color === newLabel.color){
        return [true, ""]
      }
      if(!newLabel.name){
        return [false, '标签名不应为空']
      }
      if(!newLabel.color){
        return [false, '颜色名不应为空']
      }
      for(let label of this.labels){
        if(newLabel.name === label.name && newLabel.name !== oldLabel.name){
          return [false, '标签名存在冲突']
        }
      }
      Vue.axios.put(`/datasets/labels/${newLabel.id}`, newLabel).then(()=>{
        this.loadLabels()
      })
      return [true, ""]
    },

    loadLabels(){
      this.$http.get(`/datasets/${this.datasetId}/labels`).then((response) => {
        this.labels = response.data
        this.$emit('change', response.data)
      })
    }
  },
  created() {
    if(this.datasetId){
      this.loadLabels()
    }
  }
}
</script>

<style scoped>
.label-card{
  background: #ffffff;
}
.label-item{
  margin: 15px 10px 15px 0;
  height: 40px;
}
.label-list-wrapper{
  margin-top: 10px;
  overflow-y: auto;
  max-height: 250px;
}
</style>