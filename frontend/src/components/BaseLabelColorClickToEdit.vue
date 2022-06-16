<template>
 <div class="wrapper">
   <div v-if="edit">
     <base-label-color-input
         :label="this.label"
         @cancel="edit=false"
         @change="checkAndConfirm"
     />
   </div>
<!--   $emit('change', $event.target.value)-->
   <div v-else class="label-color-wrapper">
     <div class="color-block" :style="colorObject" />
      <span class="label-name text-overflow-hidden">{{label.name}}</span>
     <div class="action-wrapper" v-if="editable">
       <i class="el-icon-edit hover-pointer hover-blue" @click="edit=true"/>
       <el-divider direction="vertical"/>
       <i class="el-icon-delete hover-pointer hover-blue" @click="$emit('delete')"/>
     </div>
   </div>
 </div>
</template>

<script>
import BaseLabelColorInput from "@/components/BaseLabelColorInput";
export default {
  name: "BaseLabelColorClickToEdit",
  components: {BaseLabelColorInput},
  props:{
    label:{
      type: Object
    },
    validator:{
      type: Function,
      default: function(){
        return true, ""
      }
    },
    editable: {
      type: Boolean,
      default: true,
    }
  },
  data(){
    return {
      edit: false,
      annotationLocal: this.label.name,
      colorLocal: this.label.color,
      labelLocal: {
        name: this.label.name,
        color: this.label.color
      }
    }
  },
  computed:{
    colorObject(){
      return{
        background: this.label.color
      }
    }
  },
  methods:{
    checkAndConfirm(value){
      let [valid, errorMessage] = this.validator(this.label, Object.assign({...this.label}, value))
      if(!valid){
        this.$message.error(errorMessage)
      }else{
        this.edit = false
      }
    },
  }
}
</script>

<style scoped lang="less">
.wrapper{
  min-width: 0;
  height: 100%;
}
.label-color-wrapper{
  display: flex;
  height: 100%;
  border: 1px solid #eee;
  border-radius: 1px;
  align-items: center;
}
.color-block{
  width: 10px;
  height: 100%;
  flex-shrink: 0;
}
.label-name{
  margin-left: 10px;
  margin-right: 10px;
  font-family: Arial;
  font-size: 18px;
}
.text-overflow-hidden{
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.action-wrapper{
  display: flex;
  margin-left: auto;
  margin-right: 10px;
}
.hover-pointer:hover{
  cursor: pointer;
}
.hover-blue:hover{
  color: dodgerblue;
}

</style>