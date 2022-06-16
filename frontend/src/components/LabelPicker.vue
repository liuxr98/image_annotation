<template>
  <el-card class="label-picker">
    <template slot="header">
      <LabelPickerHeader/>
    </template>
    <el-input
        clearable
        suffix-icon="el-icon-search"
        v-model="search"
        placeholder="请输入标签名称"
    />
    <el-divider/>
    <div v-for="label in filteredLabels" :key="label.id">
      <BaseLabelColorClickToEdit
          :editable="isLabelEditable"
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
import LabelPickerHeader from "@/components/LabelPickerHeader";

export default {
  name: "LabelPicker",
  components: {
    BaseLabelColorClickToEdit,
    LabelPickerHeader
  },
  data(){
    return {
      search: '',
    }
  },
  computed:{
    filteredLabels(){
      return this.$store.state.annotate.labels
          .filter(label => !this.search || label.name.toLowerCase().includes(this.search.toLowerCase()))
    },
    isLabelEditable(){
      // 如果是团队任务不允许成员编辑
      return !this.$store.state.annotate.isTeamWork
    }
  },
  methods:{
    deleteLabel(label_id){
      this.$store.dispatch("annotate/deleteLabel", label_id)
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
      for(let label of this.$store.state.annotate.labels){
        if(newLabel.name === label.name && newLabel.name !== oldLabel.name){
          return [false, '标签名存在冲突']
        }
      }
      this.$store.dispatch("annotate/updateLabel", newLabel)
      return [true, ""]
    }
  }
}
</script>

<style scoped lang="less">
.label-picker{
  height: 100%;
  overflow-y: hidden;
  border-left: 1px solid #eee;
  border-bottom: 1px solid #eee;
  display: flex;
  flex-direction: column;
  box-shadow: 0 2px 4px 0 rgb(0 0 0 / 15%)
}
.label-item{
  margin-top: 15px;
  height: 50px;
}

</style>