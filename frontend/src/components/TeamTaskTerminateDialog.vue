<template>
  <el-dialog
      :visible="dialogVisible"
      title="提示"
      @close="handleClose"
      width="500px"
  >
    <div class="content-wrapper">
      <div class="warning-text">
        <i class="el-icon-warning warning-icon"/>
        <span> 此操作将终止正在进行的多人任务 </span>
      </div>
      <br/>
      <div>
        <span>
            是否要保存当前已提交任务的所有标注: &ensp;
        </span>
        <el-radio-group v-model="reserved">
          <el-radio :label="true">
            是
          </el-radio>
          <el-radio :label="false">
            否
          </el-radio>
        </el-radio-group>
      </div>
    </div>
    <span slot="footer" >
      <el-button @click="handleClose">取 消</el-button>
      <el-button type="primary" @click="handleCommit">确 定</el-button>
    </span>
  </el-dialog>
</template>

<script>
export default {
  name: "TeamTaskTerminateDialog",
  props: {
    dialogVisible: {
      type: Boolean,
      default: false,
    }
  },
  data(){
    return {
      reserved: true,
    }
  },
  watch:{
    dialogVisible(val){
      if(!val){
        this.reserved = true
      }
    }
  },
  methods:{
    handleCommit(){
      this.$store.dispatch('teamTask/terminateTeamTask',{
        id: this.$store.state.teamTask.teamTaskID,
        reserved: this.reserved
      })
      this.handleClose()
    },
    handleClose(){
      this.$emit('update:dialogVisible', false)
    },
  }
}
</script>

<style scoped>
.warning-text{
  display: flex;
  align-items: center;
}
.warning-icon{
  font-size: x-large;
  color: #e6a23c;
  margin-right: 5px;
}
.content-wrapper{
  display: flex;
  flex-direction: column;
}
</style>