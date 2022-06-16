<template>
  <div v-if="empty">
    <el-empty description="暂无数据"></el-empty>
  </div>
 <div class="right-content-wrapper" v-else>
   <el-descriptions
       title="团队详情"
       size="medium"
       :column="2"
       label-class-name="my-label"
   >
      <el-descriptions-item label="团队名称" >
        {{teamInfo.name}}
      </el-descriptions-item>
      <el-descriptions-item label="团队成员数量">
        {{teamInfo.memberCnt}}
      </el-descriptions-item>
   </el-descriptions>
   <div>
     <el-button icon="el-icon-plus" size="medium" @click="dialogVisible=true">
       添加成员
     </el-button>
     <team-member-add-dialog :dialog-visible.sync="dialogVisible"/>
   </div>
   <el-table :data="teamInfo.members">
     <el-table-column label="成员名称" prop="member_name">
     </el-table-column>
     <el-table-column label="角色">
       <template slot-scope="record">
         <span>
           {{roleMap[record.row.role]}}
         </span>
       </template>
     </el-table-column>
     <el-table-column label="操作">
       <template slot-scope="record">
         <el-button type="text" @click="deleteMember(record.row.id)">删除</el-button>
       </template>
     </el-table-column>
   </el-table>
 </div>
</template>

<script>
import {mapState} from "vuex";
import TeamMemberAddDialog from "@/components/TeamMemberAddDialog";

export default {
  name: "TeamRightPanel",
  components: {TeamMemberAddDialog},
  methods:{
    deleteMember(id){
      this.$confirm(
          '此操作将删除该成员，删除无法恢复，请谨慎操作！',
          '删除成员',
          {
            type: 'warning',
            confirmButtonText: '确认',
            cancelButtonText: '取消'
          }
      ).then(()=>{
        this.$store.dispatch("team/deleteMember", id)
      }).catch(()=>{})
    }
  },
  data(){
    return {
      roleMap:{
        labeler: '标注员',
        reviewer: '审核员'
      },
      dialogVisible: false
    }
  },
  computed:{
    ...mapState('team',{
      teamInfo: "activeTeamInfo"
    }),
    empty(){
      return this.$store.getters["team/teamsLength"] === 0
    }
  },
  created() {
    this.unsubscribe = this.$store.subscribe((mutation)=>{
      if(mutation.type === 'team/setActiveIndex'){
        this.$store.dispatch("team/getTeamInfo")
      }
    })
  },
  beforeDestroy() {
    this.unsubscribe()
  }
}
</script>

<style>
.right-content-wrapper{
  padding-left: 15px;
}
.my-label{
  color: #8a8e99;
}
</style>