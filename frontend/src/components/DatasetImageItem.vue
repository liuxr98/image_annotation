<template>
  <div class="entity-item">
    <el-image
      style="width: 136px; height: 136px"
      :src="img.img_src"
      fit="contain"
      lazy
    />
    <el-checkbox class="entity-item-checkbox" @change="handleChange"></el-checkbox>
  </div>
</template>

<script>
export default {
  name: "DatasetImageItem",
  props:[
      'img'
  ],
  methods:{
    handleChange(val){
      if(val){
        this.$emit('select', this.img.id)
      }else{
        this.$emit('cancel-select', this.img.id)
      }
    }
  }
}
</script>

<style scoped lang="less">
.entity-item{
  width: 138px;
  height: 174px;
  background-color: #f6f6f6;
  border: 1px solid transparent;
  margin: 0 10px 10px 0;
  position: relative;
  &-checkbox{
    position: absolute;
    top: -3px;
    right: 0;
  }
}
</style>