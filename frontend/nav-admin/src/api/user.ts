import { http } from "@/utils/http";
import { baseUrlApi } from "./utils";

export const changeUserPassword = (data: {
  old_password: string;
  new_password: string;
}) => {
  console.log("Submitting data:", data);
  return http.request<any>("post", baseUrlApi("admin/change-password"), {
    data
  });
};
