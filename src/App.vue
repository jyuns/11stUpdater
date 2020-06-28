<template>
  <v-app>
    <v-app-bar app>
      <h3 style='color:white;'>스토어 대량 업로드</h3>
    </v-app-bar>
    <v-main>

      <div class='alert-wrapper' v-if='(this.sucAlert.length + this.errAlert.length)'>
        <v-alert type="success" v-if='this.sucAlert.length'>{{this.sucAlert}}</v-alert>
        <v-alert type="error" v-if='this.errAlert.length'>{{this.errAlert}}</v-alert>
      </div>

      <div class='login-wrapper'>
      <div class='login-form'>
        <!--11번가 로그인-->
        <v-text-field label='11번가 ID' v-model="userID" :rules='idRules' hide-details='auto' :disabled="disabledLogBtn" />
        <v-text-field label='11번가 PW' v-model="userPW" :rules='pwRules' hide-details='auto' :disabled="disabledLogBtn" />
      </div>
      <div class='log-btn-wrapper'>
        <v-btn class='log-btn' color='primary' @click='login()' :disabled="disabledLogBtn">로그인</v-btn>
        <v-btn class='log-btn' color='error' @click='logout()' :disabled="!disabledLogBtn">로그아웃</v-btn>
      </div>
      </div>

      <div class='drop-wrapper' @dragover.prevent @drop.stop.prevent="dropFile">
        <div class='drop-zone' v-if='files == null'>
          <img :src='require("./assets/upload.svg")' style='width:42px; margin-bottom:8px;' />
          폴더나 파일을 드랍해주세요
        </div>

        <div class='file-list' v-else>
          
          <div class='drop-header'>
            <span>{{Object.keys(files).length}}건의 폴더가 업로드되었습니다.</span>
            <div>
              <v-btn depressed small color="primary" @click='upload()' style='margin-right:12px;' :disabled="disabledUploadBtn">업로드</v-btn>
              <v-btn depressed small color="error" @click='reset()' :disabled="disabledUploadBtn" >취소</v-btn>
            </div>
          </div>

          <v-divider style='margin:18px 0px;' />

          <div v-for='(folder, index) in Object.keys(files)' :key='folder+index' style='margin-bottom:12px;'>
            <h5 v-show='files[folder].length'>
              <span v-if='folder==""'>바탕화면</span>
              <span v-else>{{folder}}</span>
              에서 총 {{files[folder].length}}건 업로드 되었습니다.</h5>
            <span v-for='(file, index) in files[folder].slice(0,5)' :key='file+index'>
              <h6>- {{file}}</h6>
            </span>
          </div>
        </div>
      </div>

    </v-main>
 
    <div class='progress-wrapper' v-if='uploading>0'>
      <progress-bar bar-color="#dc720f" :val="(uploading/getFileNumber)*100" :text="((uploading/getFileNumber)*100)+'%'" />
    </div>
 
  </v-app>
</template>

<script>

import ProgressBar from 'vue-simple-progress'
const JSEncrypt = require('./encrypt')

export default {
  name: 'App',

  components : {
    ProgressBar
  },

  data: () => ({

    userID : '',
    userPW : '',

    // 로그인 성공 시, 쿠키 저장
    successLogin : null,

    idRules : [
      value => !!value || '아이디를 입력해 주세요.',
      value => (value && value.length >= 3) || '아이디를 입력해 주세요.'
    ],
    pwRules : [
      value => !!value || '패스워드를 입력해 주세요.',
      value => (value && value.length >= 3) || '패스워드를 입력해 주세요.'
    ],

    files : null,

    errAlert : '',
    sucAlert : '',

    uploading : 0,

    disabledUploadBtn : false,
    disabledLogBtn : false,

    options: {
      target: 'https://wpartner.wemakeprice.com/common/uploadImageAsync.json',
      testChunks: false
    },
  }),

  computed : {
    getFileNumber() {
      const values = Object.values(this.files)
      let number = 0

      for(let i = 0; i < values.length; i++) {
        number = number + values[i].length
      }
      return number 
    }
  },

  methods : {

    async login() {
      
      if(!this.userID.length) return
      if(!this.userPW.length) return
      
      console.log()
      JSEncrypt.default.prototype.setPublic('a650c97fe917f8cc0312541fd682ca221bc19d3e345cd07c241c266aca5d117d14d3f7f322de2282ef67c0aeb7a6eaae3bdff24c3ff661700a7906503cb8b8823c42a07fa5eb46aca7edfe52cabe1f2aa393f55cf52fd5be4316bb6aab39d1d51abfd7bd3d28700e7c1ff8bbeb549632b0b76b5be86a23b39fc8d3e703889189', '10001')
      
      let encryptedID = JSEncrypt.default.prototype.encrypt(this.userID)
      let encryptedPW = JSEncrypt.default.prototype.encrypt(this.userPW)
      
      console.log(encryptedID, encryptedPW)
      let result = await this.axios.post('http://localhost:8082/11st/login', {
        userID : encryptedID,
        userPW : encryptedPW,
      })

      let temp = result.data
      temp = temp.split("'").join('"')
      temp = temp.split(", ")

      let statusCode = JSON.parse(temp[0]+'}').status
      
      temp.shift()

      let cookies = temp.join("")
      
      if(statusCode == 422) {
        this.errAlert = 'ID/PW를 다시 입력해 주세요.'
        this.setTimeAlert('err')

      } else if(statusCode == 200) {
        this.sucAlert = '로그인 되었습니다.'
        this.successLogin = cookies

        this.setTimeAlert('suc')
        
        // 로그인 버튼 잠금
        this.disabledLogBtn = true

      } else {
        this.errAlert = '알 수 없는 오류가 발생하였습니다.'
        this.setTimeAlert('err')
      }
    },

    logout() {
      this.userID = ''
      this.userPW = ''
      this.disabledLogBtn = false
      this.successLogin = null
    },

    setTimeAlert(e) {
      if(e == 'err') {
        setTimeout( () => {
          this.errAlert = ''
        }, 2000)
      } else {
        setTimeout( () => {
          this.sucAlert = ''
        }, 2000)
      }
    },

    async upload() {

      const data = this.files
      const key = Object.keys(data)

      this.uploading = 0;
      this.disabledUploadBtn = true;
      
      for( let i = 0; i < key.length; i ++) {

        for( let j = 0; j < data[key[i]].length; j++) {

          let result = await this.axios.post('http://localhost:8082/11st/upload', {
            cookies : this.successLogin,
            path : data[key[i]][j],
            type : (data[key[i]][j].split('.').pop()).toLowerCase(),
          })

          if(result.status == 200) this.uploading++;
          // 추후 에러 반환하는 파일들에 한하여 에러처리 진행할 것
        }
      }

      if(this.uploading == this.getFileNumber) {
        this.sucAlert = '모든 파일이 성공적으로 업로드되었습니다.'
        this.setTimeAlert('suc')
      }

      // init setting
      setTimeout(() => {
        this.uploading = 0
        this.disabledUploadBtn = false;
      }, 3000)
    },

    reset() {
      this.files = null
      this.$forceUpdate()      
    },

    dropFile(e) {

      if(!this.disabledLogBtn) {
        this.errAlert = '로그인 이후 업로드를 진행해 주세요.'
        this.setTimeAlert('err')        
        return
      }

      e.preventDefault()
      e.stopPropagation()
    
      let items = e.dataTransfer.items;
      for (let i=0; i<items.length; i++) {
        // webkitGetAsEntry is where the magic happens
        let item = items[i].webkitGetAsEntry();
        if (item) {
          this.readFolder(item);
        }
      }
    },

    readFolder(item, path) {
      
      path = path || "";
    
      if(item.isFile) {
        item.file( (file) => {
          
          // file type check variable
          let checkType = 0
          
          if(this.files == null) this.files = {}
          if(this.files[path] == undefined) this.files[path] = []

          // 동일 파일 제거
          if(this.files[path].indexOf(file.path) != -1) return
          
          // image type
          let type = file.name.split('.').pop()
          type = type.toLowerCase()
          
          if(type == 'jpg') checkType++
          if(type == 'png') checkType++
          if(type == 'jpeg') checkType++
          if(type == 'gif') checkType++
          if(type == 'bmp') checkType++

          // excel type 
          if(type == 'xlsx') checkType++
          if(type == 'xls') checkType++

          // 파일 타입 체크 후 최종 list push
          if(checkType > 0) this.files[path].push(file.path)
          
          // 빈 폴더 제거
          if(this.files[path].length == 0) delete this.files[path]
          
          this.$forceUpdate()
        })
      } else if (item.isDirectory) {
        let dirReader = item.createReader()
        
        dirReader.readEntries( (entries) => {
          for(let i = 0; i < entries.length; i++) {
            this.readFolder(entries[i], path + item.name + '/')
          }
        })
      }
    }

  },
};
</script>

<style scoped>

.v-app-bar {
  background: #e55!important;
}

.login-wrapper {
  display:flex;
  flex-direction: row;
  justify-content: space-between;
  padding:16px;
}

.login-form {
 width:80%; 
}

.log-btn-wrapper{
  width:20%;
  display:flex;
  flex-direction: column;
  justify-content:center;
  align-items: flex-end;
}

.log-btn {
  width: 100%;
  max-width: 100px;
  margin-top:12px;
}

.alert-wrapper {
  position: fixed;
  display: flex;
  justify-content: center;
  height: 100vh;
  align-items: center;
  width: 100%;
}

.v-alert {
  margin:8px;
  width:100%;
  max-width:600px;
}

.drop-wrapper {
  width:100%;
  height : calc(100vh - 248px);
  padding:16px;
}

.drop-zone {
  width: 100%;
  height : 100%;
  border: 1px dashed;
  align-items: center;
  display: flex;
  justify-content: center;
  flex-direction: column;
}

.drop-header {
  display:flex;
  align-items: center;
  justify-content: space-between;
}

h6 {
  font-weight: 400;
}

.progress-wrapper {
  padding:16px;
}
</style>
