<template>
  <div>
    <el-tabs
        v-model="activeName"
        type="card"
    >
      <el-tab-pane label="本地图片" name="localImage">
        <detect-local-image-tab/>
      </el-tab-pane>

    </el-tabs>
  </div>
</template>

<script>
import DetectLocalImageTab from "@/components/DetectLocalImageTab";
export default {
  name: "DetectView",
  components: {DetectLocalImageTab},
  data(){
    return {
      activeName: 'localImage'
    }
  },
  methods:{
  }
}
</script>

<style scoped>

</style>