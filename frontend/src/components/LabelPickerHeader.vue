<template>
  <div v-if="showAddLabel">
    <BaseLabelColorInput
        @cancel="showAddLabel=false"
        @change="handleAddLabelCommit"
    />
  </div>
  <div v-else-if="showImportLabelGroup">
    <el-select
        ref="pickerHeaderSelect"
        @visible-change="afterSelectedVisible"
        v-model="importedLabelGroupID"
        filterable
        placeholder="选择导入的标签组"
        :style="{width: 100 + '%'}">
      <el-option v-for="labelGroup in labelGroups" :key="labelGroup.id" :label="labelGroup.name" :value="labelGroup.id">
      </el-option>
      <div class="import-group-button-wrapper">
        <el-button type="primary" @click="handleImportLabelGroupCommit" size="mini">确认</el-button>
        <el-button @click="showImportLabelGroup=false" size="mini">取消</el-button>
      </div>
    </el-select>
  </div>
  <div v-else class="picker-header">
    <span>标签栏</span>
    <el-dropdown split-button type="primary" @click="showAddLabel=true" v-if="isAddLabelAvailable">
      添加标签
      <el-dropdown-menu slot="dropdown">
        <el-dropdown-item @click.native="showImportLabelGroup=true">导入标签组</el-dropdown-item>
      </el-dropdown-menu>
    </el-dropdown>
  </div>
</template>

<script>
import {mapState} from "vuex";
import BaseLabelColorInput from "@/components/BaseLabelColorInput";

export default {
  name: "LabelPickerHeader",
  components:{
    BaseLabelColorInput
  },
  data(){
    return{
      importedLabelGroupID: '',
      showAddLabel: false,
      showImportLabelGroup: false,
    }
  },
  watch:{
    showImportLabelGroup(val){
      if(!val) {
        // reset data
        this.importedLabelGroupID = ''
      }
    }
  },
  computed:{
    isAddLabelAvailable(){
      // 如果是团队任务不允许其导入标签组或添加新的标签
      return !this.$store.state.annotate.isTeamWork
    },
    ...mapState('labelGroup', ['labelGroups'])
  },
  methods:{
    // 在选择后保持下拉框依然可见
    afterSelectedVisible(visible){
      if(!visible){
        this.$refs.pickerHeaderSelect.visible = true
      }
    },
    handleImportLabelGroupCommit(){

      if(!this.importedLabelGroupID){
        this.$message.error('请选择导入的标签组')
        return
      }
      this.$store.dispatch('annotate/addLabels', this.importedLabelGroupID).then(response =>{
          let conflictedLabels = response.data
          if(conflictedLabels.length !== 0) {
             this.$notify({
               title: '提示',
               type: 'warning',
               message: '以下名称冲突（相同）的标签未导入：' + conflictedLabels.toString(),
               duration: 0
             });
          }
          this.$store.dispatch('annotate/getLabels')
      })
      this.showImportLabelGroup = false
    },

    handleAddLabelCommit(value) {
      if(!value.name){
        this.$message.error('标签名不能为空')
        return
      }
      if(!value.color){
        this.$message.error('颜色不能为空')
        return
      }
      // 检查添加的标签是否与数据集已有的标签重复
      for (let label of this.$store.state.annotate.labels) {
        if (label.name === value.name) {
          this.$message.error('标签重复，请修改添加的标签名称')
          return
        }
      }
      // 通过check,则提交
      this.$store.dispatch("annotate/addLabel", value)
      this.showAddLabel = false
    }
  },


}
</script>

<style scoped>
.picker-header{
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.import-group-button-wrapper{
  display: flex;
  justify-content: flex-end;
  padding-top: 5px;
  padding-right: 5px;
}
</style>