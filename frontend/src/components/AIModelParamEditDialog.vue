<template>
  <el-dialog
      :visible="dialogVisible"
      title="超参数编辑"
      width="500px"
      @close="handleClose"
  >
<!--    <el-form-->
<!--        ref="form"-->
<!--        :model="form"-->
<!--        :rules="rules"-->
<!--        label-position="right"-->
<!--        label-width="80px"-->
<!--    >-->
<!--      <el-form-item label="模型名称" prop="name">-->
<!--        <el-input v-model="form.name"></el-input>-->
<!--      </el-form-item>-->
<!--    </el-form>-->
<!--    <span slot="footer" class="dialog-footer">-->
<!--      <el-button @click="handleClose">取 消</el-button>-->
<!--      <el-button type="primary" @click="handleCommit">确 定</el-button>-->
<!--    </span>-->
    <el-alert
        :closable="false"
        title="参数编辑提示"
        type="info"
    >
      1. 你可以通过 json 文件将相关参数配置添加到模型文件中
      <br/>
      2. json 文件名会保持不变，所以可能会覆盖模型文件夹中的同名文件
      <br/>
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
  name: "AIModelParamEditDialog",
  props: {
    dialogVisible: {
      type: Boolean,
      default: false,
    },
    modelId: {
      default: ''
    }
  },
  data(){
    return{
      form: {},
      rules:{
      }
    }
  },
  // watch:{
  //   dialogVisible(val){
  //     if(!val){
  //       this.$refs.form.resetFields()
  //       this.form = {
  //       }
  //     }
  //   }
  // },
  methods:{
    handleCommit() {
      if(this.$refs.upload.uploadFiles.length === 0){
        this.$message.error('上传的文件不能为空')
        return
      }
      let formData = new FormData()
      this.$refs.upload.uploadFiles.forEach(file=>{
        formData.append('file', file.raw)
      })
      this.$http.put(`/models/${this.modelId}`, formData).then(() => {
        this.handleClose()
      })
    },

    handleClose(){
      this.$emit('update:dialogVisible', false);
    },

    hackUpload(){
      // do nothing
      // trigger beforeUpload checking
    },

    beforeUpload(file){
      console.log(file.type)
      const allowedExtension = ['application/json']
      const size10M = 10 * 1024 * 1024
      let isImage = allowedExtension.includes(file.type)
      let isLt10M = file.size < size10M
      if(!isImage || !isLt10M){
        this.$message.error('文件格式错误或大小超过限制')
        return false
      }
      return true
    },

    onExceed(){
      this.$message.error('上传的文件超出数量上限')
    }
  },
}
</script>

<style scoped>

</style>