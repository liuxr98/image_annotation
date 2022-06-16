<template>
 <el-dialog
     :visible="dialogVisible"
     title="创建多人标注任务"
     @close="handleClose"
     width="500px"
 >
   <el-form
    ref="form"
    :model="form"
    :rules="rules"
    label-width="80px"
    label-position="right"
   >
     <el-form-item label="任务名称" prop="name">
        <el-input v-model="form.name" :maxlength="30"/>
     </el-form-item>
     <el-form-item label="数据集" prop="datasetID">
        <el-select v-model="form.datasetID" style="width: 100%">
          <el-option
              v-for="dataset in datasetOptions"
              :key="dataset.id"
              :label="dataset.name"
              :value="dataset.id"
              :disabled="dataset.status !== 'None'"
          />
        </el-select>
     </el-form-item>
     <el-form-item>
       <el-alert
           type="info"
           title="已经处于多人任务以及智能标注中或暂无数据的数据集将不可选"
           show-icon
       >
       </el-alert>
     </el-form-item>
     <el-form-item v-if="form.datasetID" label="标签" prop="labels">
        <team-task-label-card :dataset-id="form.datasetID" class="label-card" v-model="form.labels"/>
     </el-form-item>
    <el-form-item>
      <el-alert
        v-if="form.datasetID"
        type="warning"
        title="尽量不要随意编辑或删除已有的标签"
        description="这可能对已经使用该标签的标注框造成影响"
        show-icon
      >
      </el-alert>
    </el-form-item>
     <el-form-item label="团队" prop="teamID">
       <el-select v-model="form.teamID" style="width: 100%">
         <el-option
            v-for="team in teamOptions"
            :key="team.id"
            :label="team.name"
            :value="team.id"
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
import TeamTaskLabelCard from "@/components/TeamTaskLabelCard";
export default {
  name: "TeamTaskCreateDialog",
  components: {TeamTaskLabelCard},
  props: {
    dialogVisible:{
      type: Boolean,
      default: false,
    }
  },
  computed:{
    datasetOptions(){
      return this.$store.state.dataset.datasets
    },
    teamOptions(){
      return this.$store.state.team.teams
    }
  },
  data(){
    return{
      form: {
        name: '',
        datasetID: '',
        teamID: '',
        labels: []
      },
      rules: {
        name: [{required: true, message: '请输入任务名称', trigger: 'blur'}],
        datasetID: [{required: true, message: '请选择标注的数据集', trigger: 'blur'}],
        teamID: [{required: true, message: '请选择团队', trigger: 'blur'}],
        labels: [{required: true, message: '标签不能为空', trigger: 'blur'}]
      }
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
  methods:{
    handleCommit(){
      this.$refs.form.validate((valid)=>{
        if(valid){
          this.$store.dispatch('teamTask/addTeamTask', this.form)
          this.handleClose()
        }
      })
    },
    handleClose(){
      this.$emit('update:dialogVisible', false)
    },
    resetFormData(){
      this.form = {
        name: '',
        datasetID: '',
        teamID: '',
        labels: []
      }
    }
  }
}
</script>

<style scoped>
.label-card{
}
</style>