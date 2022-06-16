<template>
  <el-dialog
      :visible="dialogVisible"
      title="创建团队"
      @close="handleClose"
      width="400px"
  >
    <el-form
        ref="form"
        :model="form"
        :rules="rules"
        label-position="right"
        label-width="80px"
    >
        <el-form-item label="团队名称" prop="name">
          <el-input v-model="form.name" :maxlength="30"></el-input>
        </el-form-item>
    </el-form>
    <span slot="footer" >
      <el-button @click="handleClose">取 消</el-button>
      <el-button type="primary" @click="handleCommit">确 定</el-button>
    </span>
  </el-dialog>
</template>

<script>
export default {
  name: "TeamCreateDialog",
  props: {
    dialogVisible: {
      type: Boolean,
      default: false
    }
  },
  watch:{
    dialogVisible(val){
      if(!val){
        // 清楚验证信息
        this.$refs.form.resetFields()
        // 重置数据
        this.resetFormData()
      }
    }
  },
  data(){
    let nameDuplicateValidator = (rule, value, callback) =>{
      for(let team of this.$store.state.team.teams){
        if(team.name === value){
          callback(new Error('团队名称重复，请修改'))
        }
      }
      callback()
    }
    return {
      form:{
        name: ''
      },
      rules: {
        name: [
          {required: true, message: '请输入团队名称',  trigger: 'blur'},
          {validator: nameDuplicateValidator, trigger: 'blur'}
        ]
      }
    }
  },
  methods:{
    handleClose(){
      this.$emit('update:dialogVisible', false)
    },
    handleCommit(){
      this.$refs.form.validate((valid)=>{
        if(valid){
          this.$store.dispatch('team/addTeam', this.form)
          this.handleClose()
        }
      })
    },
    resetFormData(){
      this.form = {
        name: ''
      }
    }
  }
}
</script>

<style scoped>

</style>