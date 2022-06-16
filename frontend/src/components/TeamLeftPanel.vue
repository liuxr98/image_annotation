<template>
  <div class="left-content-wrapper">
    <div class="button-wrapper">
      <el-button type="primary" plain @click="dialogVisible=true">添加团队</el-button>
      <el-button
        :disabled="disabled"
        @click="deleteTeam()"
      >
        删除
      </el-button>
    </div>
    <team-create-dialog :dialog-visible.sync="dialogVisible"/>
    <el-empty description="暂无数据" v-if="empty"/>
    <team-info-display
      v-for="(team, index) in teams"
      :key="team.id"
      :team-info="team"
      :active="activeID === team.id"
      @click.native="handleClick(index)"
    />
  </div>
</template>

<script>
import TeamInfoDisplay from "@/components/TeamInfoDisplay";
import {mapGetters, mapState} from "vuex";
import TeamCreateDialog from "@/components/TeamCreateDialog";
export default {
  name: "TeamLeftPanel",
  components: {TeamCreateDialog, TeamInfoDisplay},
  computed:{
    ...mapState("team",{
      teams: 'teams',
    }),
    ...mapGetters("team",{
      activeID: 'activeTeamID'
    }),
    disabled(){
      return this.$store.getters["team/teamsLength"] === 0
    },
    empty(){
      return this.$store.getters["team/teamsLength"] === 0
    }
  },
  data(){
    return{
      dialogVisible: false
    }
  },
  methods:{
    handleClick(index){
      // 如果点击未改变，则直接返回
      if(index === this.$store.state.team.activeIndex){
        return
      }
      this.$store.commit("team/setActiveIndex", index)
    },
    deleteTeam(){
      this.$confirm(
          '此操作将删除该团队及所有成员，删除无法恢复，请谨慎操作！',
          '删除团队',
          {
            type: 'warning',
            confirmButtonText: '确认',
            cancelButtonText: '取消'
          }
      ).then(()=>{
        this.$store.dispatch('team/deleteTeam')
      }).catch(()=>{})
    }
  },
}
</script>

<style scoped>
.button-wrapper{
  display: flex;
  justify-content: flex-start;
}
.left-content-wrapper{
  display: flex;
  flex-direction: column;
  padding-right: 10px;
}
</style>