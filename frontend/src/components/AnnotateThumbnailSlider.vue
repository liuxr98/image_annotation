<template>
 <div class="carousel" ref="carousel">
   <swiper :options="swiperOptions" ref="mySwiper">
     <swiper-slide
         v-for="(img, index) in imgList"
         :key="index"
         :class="{active: activeIndex === index}">
       <img @click="clickImage(index)" :src="img.img_src" class="swiper-item"/>
     </swiper-slide>
     <div class="swiper-button-prev swiper-button-black" slot="button-prev"></div>
     <div class="swiper-button-next swiper-button-black" slot="button-next"></div>
   </swiper>
 </div>
</template>

<script>
import {Swiper, SwiperSlide} from 'vue-awesome-swiper'
import 'swiper/css/swiper.css'

export default {
  name: "AnnotateThumbnailSlider",
  components:{
    Swiper,
    SwiperSlide
  },

  computed:{
   imgList(){
     return this.$store.getters["annotate/thumbnailImageList"]
   },
   activeIndex(){
      return this.$store.state.annotate.activeIndex
   }
  },

  data(){
    return {
      swiperOptions:{
        spaceBetween: 10,
        freeMode: true,
        slidesPerView: 'auto',
        // 最好设置成 PerView - 1
        slidesPerGroup: 5,
        navigation: {
          nextEl: '.swiper-button-next',
          prevEl: '.swiper-button-prev'
        }
      }
    }
  },
  methods:{
    clickImage(index){
      // 如果点击的是正在标注的图片，那么无需更改 activeIndex
      if(index === this.$store.state.annotate.activeIndex){
        return
      }
      this.$store.dispatch("annotate/checkAndSave").then((valid) =>{
          if(valid){
            // 保存成功才能跳转
            this.$store.commit("annotate/setActiveIndex", index)
          }else{
            this.$message({
              message: '所有标注框必须设置标签',
              type: 'warning'
            })
          }
        })
    }
  },
}
</script>

<style scoped lang="less">
.carousel{
  height: 150px;
  width: 100%;
}
.swiper-container{
  height: 100%;
  padding: 10px 0;
  box-sizing: border-box;
  .swiper-slide{
    //设置成border-box，否则最后一个slide会有部分被遮挡
    box-sizing: border-box;
    border: 2px solid #eeeeee;
    height: 100%;
    width: 200px;
  }
  .active{
    border: #1a73e8 solid 2px;
  }
}
.swiper-item{
  width: 100%;
  height: 100%;
  background: #f7f7f7;
  object-fit: contain;
}

</style>