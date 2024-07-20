import { http } from "@/utils/http";
import { baseUrlApi } from "./utils";

export const changeUserPassword = (data?: object) => {
  return http.request<any>("post", baseUrlApi("admin/change-password"), data);
};
