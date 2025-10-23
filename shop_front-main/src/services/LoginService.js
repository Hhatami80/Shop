import api from "./AxiosService"


export const loginService = {
  login(payload) {
    return api.post('/sign-in', payload, {
      headers :{
        'Accept':'application/json'
      }
    })
  },
  logout(){
    return api.put('/sign-out')
  }
}

