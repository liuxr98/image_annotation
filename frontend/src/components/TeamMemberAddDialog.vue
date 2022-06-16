<template>
  <el-dialog
      :visible="dialogVisible"
      title="添加成员"
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
      <el-form-item label="成员名称" prop="name">
        <el-input v-model="form.name"></el-input>
      </el-form-item>
      <el-form-item label="成员角色" prop="role">
        <el-select v-model="form.role" style="width: 100%">
          <el-option
              v-for="item in roleOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
          />
        </el-select>
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
  name: "TeamMemberAddDialog",
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
    let nameValidator = (rule, value, callback) =>{
      // check name duplicate
      for(let member of this.$store.state.team.activeTeamInfo.members){
        if(member.member_name === value){
          callback(new Error('成员重复，请修改'))
        }
      }
      // check existence
      this.$http.get(`/users/existence/${value}`).then((response)=>{
        if(response.data){
          callback()
        }else{
          callback(new Error('添加的用户不存在'))
        }
      })
    }
    return {
      form:{
        name: '',
        role: 'labeler' //default value
      },
      roleOptions:[
        {
          value: 'labeler',
          label: '标注员',
        },
        // {
        //   value: 'reviewer',
        //   label: '审核员'
        // }
      ],
      rules: {
        name: [
          {required: true, message: '请输入团队成员名称',  trigger: 'blur'},
          {validator: nameValidator, trigger: 'blur'}
        ],
        role:[
          {required: true, message: '请选择角色', trigger: 'blur'}
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
          this.$store.dispatch('team/addMember', this.form)
          this.handleClose()
        }
      })
    },
    resetFormData(){
      this.form = {
        name: '',
        role: 'labeler'
      }
    }
  }
}
</script>

<style scoped>

</style>