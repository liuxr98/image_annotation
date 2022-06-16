<template>
  <div class="team-info-display" :class="{'select-active': active}">
    <div class="team-text-label text-overflow-hidden">
      {{teamInfo.name}}
    </div>
    <div class="team-summary-info">
      <i class="el-icon-user text-overflow-hidden member-number">
        {{teamInfo.memberCnt}}
      </i>
    </div>
  </div>
</template>

<script>
export default {
  name: "TeamInfoDisplay",
  props: {
    active:{
      type: Boolean,
      default: false
    },
    teamInfo:{
      type: Object
    }
  },
}
</script>

<style scoped>
.team-info-display{
  height: 68px;
  border: 1px solid #ddd;
  margin: 5px 0;
  padding: 10px 15px;
  cursor: pointer;
  box-sizing: border-box;
}
.select-active{
  border-color: #39f;
  border-left: 3px solid #39f;
  padding-left: 13px;
}
.team-text-label{
  width: 90%;
  font-weight: bold;
}
.text-overflow-hidden{
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.team-summary-info{
  margin-top: 10px;
  width: 100%;
  display: flex;
}
.member-number{
  width: 60px;
}
</style>