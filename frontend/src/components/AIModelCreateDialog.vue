<template>
 <el-dialog
     :visible="dialogVisible"
     title="导入模型"
     width="500px"
     @close="handleClose"
 >
   <el-form
    ref="form"
    :model="form"
    :rules="rules"
    label-position="right"
    label-width="100px"
   >
     <el-form-item label="模型名称" prop="name">
       <el-input v-model="form.name" :maxlength="30"></el-input>
     </el-form-item>
     <el-form-item label="项目根文件夹" prop="projName">
       <el-input v-model="form.projName" :maxlength="128"></el-input>
     </el-form-item>
     <el-alert
         :closable="false"
         title="关于项目根文件名称"
         type="warning"
     >
       1. 不指定项目根文件名称时，将会默认使用 zip 文件名称作为项目根文件夹名，例如你提交的 zip 文件名为 test.zip，
       将默认认为项目根文件夹名为 test，即 train.py 在 test 目录下
       <br/><br/>
       2. 当 zip 文件夹名称与项目根文件名称不一致时，请务必指定正确的项目根文件夹名，否则会找不到相应的路径。例如你提交的为 test2.zip，
       而项目根文件名为 test，项目根文件夹应该填写为 test
       <br/>
     </el-alert>
      <el-form-item label="上传模型">
        <el-upload
          ref="upload"
          accept="application/zip,application/x-zip-compressed"
          action="someAction"
          :limit="1"
          :http-request="hackUpload"
          :before-upload="beforeUpload"
          :on-exceed="onExceed"
        >
          <div class="upload-text">
            <i class="el-icon-upload" style="font-size: xx-large"></i>
            <span style="">&ensp;点击上传模型Zip文件</span>
          </div>
        </el-upload>
      </el-form-item>
   </el-form>
   <span slot="footer" class="dialog-footer">
      <el-button @click="handleClose">取 消</el-button>
      <el-button type="primary" @click="handleCommit">确 定</el-button>
    </span>
 </el-dialog>
</template>

<script>
export default {
  name: "AIModelCreateDialog",
  props: {
    dialogVisible: {
      type: Boolean,
      default: false,
    }
  },
  data(){
    let nameDuplicateValidator = (rule, value, callback) =>{
      for(let model of this.$store.state.model.models){
        if(model.name === value){
          callback(new Error('模型名称重复,请修改'))
        }
      }
      callback()
    }
    return{
      form:{
        name: '',
        projName: ''
      },
      rules:{
        name: [
          {required: true, message: '请输入模型名称', trigger: 'blur'},
          {validator: nameDuplicateValidator, trigger: 'blur'}
        ],
      }
    }
  },
  watch:{
    dialogVisible(val){
      if(!val){
        this.$refs.form.resetFields()
        this.form = {
          name: '',
          projName: ''
        }
        this.$refs.upload.clearFiles()
      }
    }
  },
  methods:{
    handleCommit() {
      this.$refs.form.validate((valid)=>{
        if(valid){
          if(this.$refs.upload.uploadFiles.length === 0){
            this.$message.error('上传的文件不能为空')
            return
          }
          this.handleClose()
          let formData = new FormData()
          this.$refs.upload.uploadFiles.forEach(file=>{
            formData.append('file', file.raw)
          })
          formData.append('name', this.form.name)
          formData.append('projName', this.form.projName)
          this.$http.post(`/models/`, formData).then(() => {
            this.$store.dispatch('model/getModels')
          })
        }
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
      const allowedExtension = ['application/zip', 'application/x-zip-compressed']
      const size1G = 1027 * 1024 * 1024 * 1
      let isZip = allowedExtension.includes(file.type)
      let isLt5G = file.size < size1G
      if(!isZip || !isLt5G){
        this.$message.error('文件格式错误或大小超过限制')
        return false
      }
      return true
    },
    onExceed(){
      this.$message.error('上传的文件超出数量上限')
    }
  },
  // created() {
  //   this.$nextTick(() => {
  //     document.getElementsByClassName(
  //         "el-upload__input"
  //     )[0].webkitdirectory = true;
  //   });
  // }
}
</script>

<style scoped>
.upload-text{
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>