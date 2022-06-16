<template>
  <el-table :data="tableData">
    <el-table-column
        label="任务名称"
        prop="team_task_name"
    />
    <el-table-column
        label="任务发布者"
        prop="assigner_username"
    />
    <el-table-column
        label="任务状态"
    >
      <template slot-scope="record">
        <span :style="{color: statusMap[record.row.status].color}">●&nbsp;</span>
        <span>{{statusMap[record.row.status].value}}</span>
      </template>
    </el-table-column>
    <el-table-column
        label="创建时间"
        prop="created_at"
    />
    <el-table-column label="操作">
      <template slot-scope="record" v-if="record.row.status === 'InProgress'">
        <el-button type="text" @click="handleAnnotate(record.row)">
          启动标注
        </el-button>
        <el-button type="text" @click="handleSubmit(record.row.id)">
          提交任务
        </el-button>
      </template>
    </el-table-column>
  </el-table>
</template>

<script>
import {taskTypes} from "@/util/enum";

export default {
  name: "TeamSubtaskTable",
  computed:{
    tableData(){
      return this.$store.state.teamTask.subtasks
    }
  },
  data(){
    return {
      statusMap: {
        InProgress: {
          value: '进行中',
          color: '#11b864'
          // color: '#fa920a'
        },
        Submitted: {
          value: '已提交',
          color: '#11b864'
        },
        Terminated:{
          value: '已终止',
          color: '#11b864'
        },
        Deleted:  {
          value: '已删除',
          color: '#e64552'
        }
      },
    }
  },
  methods:{
   handleAnnotate(subtaskInfo){
     this.$store.commit('annotate/setTaskType', taskTypes.TeamWork)
     this.$store.commit('annotate/setSubtaskID', subtaskInfo.id)
     this.$store.commit('annotate/setDatasetID', subtaskInfo.dataset_id)
   },
    handleSubmit(id){
     this.$store.dispatch('teamTask/submitSubtask', id)
    }
  },
}
</script>

<style scoped>

</style>