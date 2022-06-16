<template>
  <div class="__label-color-wrapper">
    <el-color-picker class="color-picker" v-model="colorLocal" :predefine="predefineColors"/>
    <el-input v-model="annotationLocal" class="input-font-big">
      <div slot="suffix" class="edit-wrapper">
        <div class="edit-action">
          <el-divider direction="vertical"/>
          <span :style="{marginRight: 5+'px', color: 'dodgerblue'}" class="hover-pointer" @click="onConfirm">确认</span>
          <span class="hover-pointer" @click="$emit('cancel')">取消</span>
        </div>
      </div>
    </el-input>
  </div>
</template>

<script>
export default {
  name: "BaseLabelColorInput",
  model: {
    prop: 'label',
    event: 'change'
  },
  props: {
    label: {
      type: Object,
      default: function (){
        return {
          name: '',
          color: '#409EFF'
        }
      }
    }
  },
  data(){
    return{
      annotationLocal: this.label.name ,
      colorLocal: this.label.color,
      predefineColors: [
        '#ff4500',
        '#ff8c00',
        '#ffd700',
        '#90ee90',
        '#00ced1',
        '#1e90ff',
        '#c71585',
      ]
    }
  },
  methods:{
    onConfirm(){
      this.$emit("change",{
        name: this.annotationLocal,
        color: this.colorLocal
      })
    }
  }
}
</script>

<style scoped>
.__label-color-wrapper{
  display: flex;
  height: 100%;
  align-items: center;
}
.hover-pointer:hover{
  cursor: pointer;
}
.color-picker{
  margin-right: 5px;
}
.edit-wrapper{
  height: 100%;
  display: flex;
  align-items: center;
}
.edit-action{
  display: flex;
  align-items: center;
}
.input-font-big ::v-deep .el-input__inner{
  font-size: 18px !important;
}
</style>