<template>
  <div>
      <el-upload
        :show-file-list="false"
        accept="image/jpeg,image/png,image/bmp"
        action="someAction"
        :http-request="uploadImage"
      >
        <el-button size="small" type="primary">点击上传</el-button>
      </el-upload>
    <br/>
    <el-image
        v-loading="loading"
        fit="contain"
        element-loading-text="拼命加载中"
        element-loading-spinner="el-icon-loading"
        element-loading-background="rgba(0, 0, 0, 0.8)"
        class="detected-image"
        :src="toBeDetectedImage"
    >
      <div slot="error" class="image-slot">
        <el-empty/>
      </div>
    </el-image>
  </div>
</template>

<script>
export default {
  name: "DetectLocalImageTab",
  data(){
    return {
      toBeDetectedImage: "",
      loading: false
    }
  },
  methods:{
   uploadImage(params){
      if(!this.beforeUpload(params.file)){
        return
      }
      this.loading = true
      let formData = new FormData()
      formData.append('file', params.file)
      this.$http.post(`/detection/`, formData).then(response => {
        this.loading = false
        this.toBeDetectedImage = 'data:image/jpeg;base64,' + response.data[0]
      })
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
  }
}
</script>

<style scoped>
.detected-image{
  width: 800px;
  height: 600px;
  border: 1px solid #8a8e99;
}
</style>