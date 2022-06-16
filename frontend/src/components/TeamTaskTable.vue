<template>
  <div>
    <team-task-terminate-dialog :dialog-visible.sync="terminateDialogVisible"/>
    <el-table :data="tableData">
      <el-table-column
          label="任务名称"
          prop="name"
      />
      <el-table-column
          label="来源数据集"
          prop="dataset_name"
      />
      <el-table-column label="任务状态">
        <template slot-scope="record">
          <span :style="{color: statusMap[record.row.status].color}">●&nbsp;</span>
          <span>{{statusMap[record.row.status].value}}</span>
          <span v-if="record.row.status === 'InProgress'">&nbsp;{{record.row.subtask_submitted_num}} / {{record.row.subtask_num}}</span>
        </template>
      </el-table-column>
      <el-table-column
          label="创建时间"
          prop="created_at"
      />
      <el-table-column label="操作">
        <template slot-scope="record">
          <el-button type="text" v-if="record.row.status === 'InProgress'" @click="handleTerminate(record.row.id)">
            终止任务
          </el-button>
          <el-button type="text" v-if="reviewOperationVisible(record.row.status)" @click="handleReview(record.row)">
            验收任务
          </el-button>
          <el-button type="text" @click="deleteTeamTask(record.row.id)">
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import {taskTypes} from "@/util/enum";
import TeamTaskTerminateDialog from "@/components/TeamTaskTerminateDialog";

export default {
  name: "TeamTaskTable",
  components: {TeamTaskTerminateDialog},
  computed:{
    tableData(){
      return this.$store.state.teamTask.teamTasks
    },
  },
  data(){
    return {
      statusMap: {
        InProgress: {
          value: '进行中',
          color: '#11b864'
          // color: '#fa920a'
        },
        Finished: {
          value: '已全部提交',
          color: '#11b864'
        },
        TerminatedReserved: {
          value: '已终止（标注保留）',
          color: '#11b864'
        },
        TerminatedUnreserved:{
          value: '已终止（不保留标注）',
          color: '#11b864'
        },
        Reviewed:{
          value: '完成验收',
              color: '#11b864'
        }
      },
      terminateDialogVisible: false
    }
  },
  methods:{
    deleteTeamTask(id){
      this.$store.dispatch('teamTask/deleteTeamTask', id)
    },
    handleReview(taskInfo){
      this.$store.commit('annotate/setTaskType', taskTypes.Review)
      this.$store.commit('annotate/setDatasetID', taskInfo.dataset_id)
      this.$store.commit('annotate/setTeamTaskID', taskInfo.id)
    },
    handleTerminate(id){
      this.$store.commit('teamTask/setTeamTaskID', id)
      this.terminateDialogVisible = true
    },
    reviewOperationVisible(status){
      return ['Finished', 'TerminatedReserved'].includes(status)
    }
  }
}
</script>

<style scoped>

</style>