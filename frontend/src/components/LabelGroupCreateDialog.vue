<template>
 <el-dialog
     :visible="dialogVisible"
     title="创建标签组"
     width="500px"
     @close="handleClose"
 >
   <el-form
       ref="form"
       :model="form"
       label-position="right"
       label-width="120px"
       :rules="rules"
   >
     <el-form-item label="标签组名称" prop="name" >
        <el-input v-model="form.name" :maxlength="30"></el-input>
     </el-form-item>
     <template v-for="(label, index) in form.labels">
       <el-form-item
           :label="index === 0 ? '标签' : ''"
           :prop="`labels[${index}]`"
            :rules="labelRule"
           :key="index">
         <el-row :gutter="5">
           <el-col :span="16">
             <el-input v-model="label.name"/>
           </el-col>
           <el-col :span="4">
             <el-color-picker v-model="label.color"/>
           </el-col>
           <el-col :span="2">
             <el-button icon="el-icon-delete"  @click="removeLabel(index)" type="text" :disabled="form.labels.length === 1"></el-button>
           </el-col>
         </el-row>
       </el-form-item>
     </template>
     <el-form-item>
       <el-button
           icon="el-icon-circle-plus-outline"
           type="primary"
           plain
           @click="addLabel"
       >
         添加标签
       </el-button>
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
  name: "LabelGroupCreateDialog",
  props: {
    dialogVisible: {
      type: Boolean,
      default: false,
    }
  },
  data(){
    // 由于标签数据是动态数据，所以专门设置了validator
    let labelValidator = (rule, value, callback) =>{
      let labelIndex = parseInt(rule.field.slice(7, -1))
      if(!value.name){
        callback(new Error('请输入标签名称'))
      }
      if(!value.color){
        callback(new Error('请选择标签颜色'))
      }
      for(let i = 0; i < labelIndex; i++){
        if(this.form.labels[i].name === value.name){
          callback(new Error('标签重复，请修改'))
        }
      }
      callback()
    }
    let labelGroupNameDuplicateValidator = (rule, value, callback)=>{
      for(let labelGroup of this.$store.state.labelGroup.labelGroups){
        if(labelGroup.name === value){
          callback(new Error('标签组名称重复，请修改'))
        }
      }
      callback()
    }
    return{
      labelRule: {
        validator: labelValidator,
        trigger: 'blur'
      },
      rules:{
        name:[
          {required: true, message: '请输入标签组名称' ,trigger:'blur'},
          {validator: labelGroupNameDuplicateValidator ,trigger:'blur'}
        ]
      },
      form:{
        name: '',
        labels: [
          {
            name:'',
            color: '#409EFF'
          },
        ]
      }
    }
  },

  watch:{
    dialogVisible(val){
      if(!val){
        // 清除验证信息
        this.$refs.form.resetFields()
        // 重置数据
        this.resetFormData()
      }
    }
  },


  methods:{
    addLabel(){
      this.form.labels.push({
        name: '',
        color:'#409EFF'
      })
    },
    removeLabel(index){
      this.form.labels.splice(index, 1)
    },

    handleClose(){
      this.$emit('update:dialogVisible', false);
    },
    handleCommit(){
      this.$refs.form.validate((valid) =>{
        if(valid){
          this.$store.dispatch('labelGroup/addLabelGroup', this.form)
          this.handleClose()
        }else{
          return false
        }
      })
    },
    resetFormData(){
      this.form = {
        name: '',
        labels: [
          {
            name:'',
            color: '#409EFF'
          },
        ]
      }
    }
  }
}
</script>

<style scoped>
</style>