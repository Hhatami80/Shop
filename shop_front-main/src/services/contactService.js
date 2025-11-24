import api from "./AxiosService";

export const contactService = {
  getInfo() {
    return api.get("/contact-info");
  },

  sendMessage(data) {
    return api.post("/contact-messages", data);
  },
  updateInfo(data) {
  return api.put("/contact-info", data);
}

};
