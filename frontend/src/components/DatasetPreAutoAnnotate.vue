<template>
  <el-dialog
    :visible="visible"
    title="智能预标注"
    width="550px"
    @close="handleClose"
  >
    <el-alert
      :closable="false"
      title="提示"
      type="warning"
      show-icon
    >
      1. 目前智能标注仅支持 Yolov5 模型
      <br/><br/>
      2. 请确保当前数据集已有的标签包含所选模型的标签，否则可能会出现漏标情况
      <br/><br/>
      3. 智能预标注结束后可通过人工进行修正
    </el-alert>
    <span slot="footer" class="dialog-footer">
      <el-button @click="handleClose">取 消</el-button>
      <el-button type="primary" @click="handleConfirm">确 定</el-button>
    </span>
  </el-dialog>
</template>

<script>
export default {
  name: "DatasetPreAutoAnnotate",
  props:{
    visible:{
      type: Boolean,
      default: false
    },
    datasetId: {
      default: ''
    }
  },
  methods:{
    handleClose(){
      this.$emit('update:visible', false);
    },
    handleConfirm(){
      this.$http.put(`/datasets/auto/${this.datasetId}`).then(()=>{
        this.handleClose()
      })
    }
  }
}
</script>

<style scoped>

</style>