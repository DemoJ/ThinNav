import { reactive } from "vue";
import type { FormRules } from "element-plus";

/** 密码正则（密码格式应为6-18位数字、字母、符号） */
export const REGEXP_PWD = /^[0-9a-zA-Z!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]{6,18}$/;

/** 登录校验 */
const loginRules = reactive(<FormRules>{
  password: [
    {
      validator: (rule, value, callback) => {
        if (value === "") {
          callback(new Error("请输入密码"));
        } else if (!REGEXP_PWD.test(value)) {
          callback(
            new Error("密码格式应为6-18位数字、字母、符号")
          );
        } else {
          callback();
        }
      },
      trigger: "blur"
    }
  ]
});

export { loginRules };
