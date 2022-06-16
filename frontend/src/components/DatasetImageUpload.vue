<template>
  <el-dialog
    :visible="visible"
    title="图片导入"
    width="550px"
    @close="handleClose"
  >
    <el-tabs type="card" v-model="activeName">
      <el-tab-pane label="上传图片" name="imageUpload">
        <el-alert
            :closable="false"
            title="上传提示"
            type="info"
            show-icon>
          1. 你可以按住 ctrl 选中多个文件
          <br/>
          2. 图片类型为 jpg/png/bmp/jpeg，单次上传限制 100 个文件
          <br/>
          3. 单张图片大小限制在 10M 内
        </el-alert>
        <br/>
        <div class="upload-wrapper">
          <el-upload
              ref="upload"
              accept="image/jpeg,image/png,image/bmp"
              action="someAction"
              :limit="100"
              :http-request="hackUpload"
              :before-upload="beforeUpload"
              :on-exceed="onExceed"
              list-type="picture-card"
              multiple
          >
            <div class="upload-text">
              <i class="el-icon-upload"></i>
              <span>&ensp;点击上传图片</span>
            </div>
          </el-upload>
        </div>
      </el-tab-pane>
      <el-tab-pane label="上传压缩包" name="zipUpload">
        <el-alert
            :closable="false"
            title="上传提示"
            type="info"
            show-icon>
          1. 压缩包仅支持 zip 格式，大小限制为 5GB 内
          <br/>
          2. 压缩包内图片类型为 jpg/png/bmp/jpeg
        </el-alert>
        <br/>
        <el-upload
            ref="zipUpload"
            accept="application/zip,application/x-zip-compressed"
            action="someAction"
            :limit="1"
            :http-request="hackUpload"
            :before-upload="beforeZipUpload"
            :on-exceed="onExceed"
        >
            <div class="upload-text">
                <i class="el-icon-upload" style="font-size: xx-large"></i>
                <span style="">&ensp;点击上传Zip文件</span>
            </div>
        </el-upload>
      </el-tab-pane>
    </el-tabs>

      <span slot="footer" class="dialog-footer">
        <el-button @click="handleClose">取 消</el-button>
        <el-button type="primary" @click="handleCommit">确 定</el-button>
      </span>
  </el-dialog>
</template>

<script>
export default {
  name: "DatasetImageUpload",
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
    return {
      activeName: 'imageUpload'
    }
  },
  watch:{
    visible(val){
      if(!val){
        this.$refs.upload.clearFiles()
        this.$refs.zipUpload.clearFiles()
        this.activeName = 'imageUpload'
      }
    }
  },
  computed:{
  },
  methods:{
    handleClose(){
      this.$emit('update:visible', false);
    },
    handleCommit(){
      this.uploadFile()
    },

    hackUpload(){
      // do nothing
      // trigger beforeUpload checking
    },

    uploadFile(){
      if(this.activeName === 'imageUpload'){
        if(this.$refs.upload.uploadFiles.length === 0){
          this.$message.error('上传的文件不能为空')
          return
        }
        this.handleClose()
        let formData = new FormData()
        this.$refs.upload.uploadFiles.forEach(file=>{
          formData.append('file', file.raw)
        })
        this.$http.post(`/datasets/${this.datasetId}/images?format=image`, formData).then(response => {
          console.log(response)
        })
      }else{
        if(this.$refs.zipUpload.uploadFiles.length === 0){
          this.$message.error('上传的文件不能为空')
          return
        }
        this.handleClose()
        let formData = new FormData()
        this.$refs.zipUpload.uploadFiles.forEach(file=>{
          formData.append('file', file.raw)
        })
        this.$http.post(`/datasets/${this.datasetId}/images?format=zip`, formData).then(response => {
          console.log(response)
        })
      }

    },

    beforeUpload(file){
      const allowedExtension = ['image/jpeg', 'image/png', 'image/bmp']
      const size10M = 10 * 1024 * 1024
      let isImage = allowedExtension.includes(file.type)
      let isLt10M = file.size < size10M
      if(!isImage || !isLt10M){
        this.$message.error('文件格式错误或大小超过限制')
        return false
      }
      return true
    },

    beforeZipUpload(file){
      const allowedExtension = ['application/zip', 'application/x-zip-compressed']
      const size5G = 1027 * 1024 * 1024 * 5
      let isZip = allowedExtension.includes(file.type)
      let isLt5G = file.size < size5G
      if(!isZip || !isLt5G){
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
.upload-wrapper{
  max-height: 320px;
  overflow-y: auto;
  height: 320px;
  background-color: #f7f7f7;
  padding: 10px;
}
.upload-text{
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>