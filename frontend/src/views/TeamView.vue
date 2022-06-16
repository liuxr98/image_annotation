<template>
 <div class="content-wrapper">
    <div class="left-panel">
      <team-left-panel/>
    </div>
   <el-divider direction="vertical"/>
   <div class="right-panel">
    <team-right-panel/>
   </div>
 </div>
</template>

<script>
import TeamLeftPanel from "@/components/TeamLeftPanel";
import TeamRightPanel from "@/components/TeamRightPanel";
export default {
  name: "TeamView",
  components: {TeamRightPanel, TeamLeftPanel},
  created() {
    this.$store.dispatch("team/getTeams").then(()=>{
      if(this.$store.getters["team/teamsLength"] !== 0){
        this.$store.commit("team/setActiveIndex", 0) // 默认显示第一个团队
      }
    })
  }
}
</script>

<style scoped>
.content-wrapper{
  width: 100%;
  display: flex;
}
.left-panel{
  width: 290px;
  max-width: 290px;
  min-width: 290px;
  flex: 0 0 290px
}
.right-panel{
  width: 0;
  height: 1000px;
  flex: 1;
}
.el-divider--vertical{
  height: 1000px;
}
</style>