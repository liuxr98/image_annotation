<template>
  <el-dialog
    :visible="visible"
    title="自定义标签 json 文件导入"
    width="550px"
    @close="handleClose"
  >
    <el-alert
      :closable="false"
      title="自定义标签提示"
      type="info"
    >
      1. 你可以通过 json 文件给标签添加除了标注名以外的额外信息
      <br/>
      2. 除非真的有这样的需求，否则不建议使用该功能
      <br/>
      3. <b>type</b> 支持 <b>Select/Input/DateTimePicker</b> 三种类型，其中 <b>Select</b> 需要定义可取值范围 <b>fields</b>
      <br/><br/>
      示例：
      <br/>
      <json-viewer
          :value="infoText"
          :expand-depth="5"
          copyable
          boxed
      >
      </json-viewer>
    </el-alert>
    <br/>
    <el-upload
        ref="upload"
        accept="application/json"
        action="someAction"
        :limit="1"
        :http-request="hackUpload"
        :before-upload="beforeUpload"
        :on-exceed="onExceed"
    >
      <div class="upload-text">
        <i class="el-icon-upload"></i>
        <span>&ensp;点击上传 json 文件</span>
      </div>
    </el-upload>
    <span slot="footer" class="dialog-footer">
      <el-button @click="handleClose">取 消</el-button>
      <el-button type="primary" @click="handleCommit">确 定</el-button>
    </span>
  </el-dialog>
</template>

<script>
export default {
  name: "DatasetLabelAdditionalLabelImport",
  props:{
    visible: {
      type: Boolean,
      default: false,
    },
    datasetId:{
      default: ''
    }
  },
  data(){
    return{
      infoText: {
        "国家地区":{
          "type": "Select",
          "fields": ["中国", "日本"]
        },
        "目标名称":{
          "type": "Input"
        },
        "时间":{
          "type": "DateTimePicker"
        }
      }
    }
  },
  methods:{
    handleClose(){
      this.$emit('update:visible', false);
    },
    handleCommit(){
      if(this.$refs.upload.uploadFiles.length === 0){
        this.$message.error('上传的文件不能为空')
        return
      }
      let formData = new FormData()
      this.$refs.upload.uploadFiles.forEach(file=>{
        formData.append('file', file.raw)
      })
      this.$http.put(`/datasets/${this.datasetId}`, formData).then(() => {
        this.handleClose()
      })
    },

    hackUpload(){
      // do nothing
      // trigger beforeUpload checking
    },

    beforeUpload(file){
      console.log(file.type)
      const allowedExtension = ['application/json']
      const size2M = 2 * 1024 * 1024
      let isImage = allowedExtension.includes(file.type)
      let isLt2M = file.size < size2M
      if(!isImage || !isLt2M){
        this.$message.error('文件格式错误或大小超过限制')
        return false
      }
      return true
    },

    onExceed(){
      this.$message.error('上传的文件超出数量上限')
    }
  }

}
</script>

<style scoped>

</style>