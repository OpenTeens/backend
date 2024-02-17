def sendEmail(target, uri):
    """
    发送验证邮件
    """

    template = """
    <!DOCTYPE html>
<html lang="en" xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <title>邮箱验证码</title>
    <style>
        table {
            width: 700px;
            margin: 0 auto;
        }
        #top {
            width: 700px;
            border-bottom: 1px solid #ccc;
            margin: 0 auto 30px;
            text-align: center;
        }
        #top table {
            font: 12px Tahoma, Arial, 宋体;
            height: 40px;
        }
        #content {
            width: 680px;
            padding: 0 10px;
            margin: 0 auto;
        }
        #content_top {
            line-height: 1.5;
            font-size: 16px;
            margin-bottom: 25px;
            color: #4d4d4d;
        }
        #content_top strong {
            display: block;
            margin-bottom: 15px;
        }
        #content_top strong span {
            color: #f60;
            font-size: 16px;
        }
        #verificationCode {
            color: #f60;
            font-size: 24px;
        }
        #content_bottom {
            margin-bottom: 30px;
        }
        #content_bottom small {
            display: block;
            margin-bottom: 20px;
            font-size: 12px;
            color: #747474;
        }
        #bottom {
            width: 700px;
            margin: 0 auto;
        }
        #bottom div {
            padding: 10px 10px 0;
            border-top: 1px solid #ccc;
            color: #747474;
            margin-bottom: 20px;
            line-height: 1.3em;
            font-size: 12px;
        }
        #content_top strong span {
            font-size: 18px;
            color: #FE4F70;
        }
        #sign {
            text-align: right;
            font-size: 18px;
            color: #367ceb;
            font-weight: bold;
        }
        #verificationCode {
            height: 100px;
            width: 680px;
            text-align: center;
            margin: 30px 0;
        }
        #verificationCode div {
            height: 100px;
            width: 680px;
        }
        .button {
            color: #367ceb;
            margin-left: 10px;
            resize: none;
            font-size: 30px;
            font-weight: bold;
            border: none;
            outline: none;
            padding: 10px 15px;
            background: #4aa5eb47;
            text-align: center;
            border-radius: 17px;
            box-shadow: 6px 6px 12px #cccccc, -6px -6px 12px #ffffff;
        }
        .button:hover {
            box-shadow: inset 6px 6px 4px #d1d1d1,
            inset -6px -6px 4px #ffffff;
        }
        img {
            max-width: 50vw;
            max-height: 50vh;
        }
    </style>
</head>
<body>
<table>
    <tbody>
    <tr>
        <td>
            <div id="top">
                <table>
                    <tbody><tr><td><img src="https://openteens.org/img/logo/v1.1.png"></td></tr></tbody>
                </table>
            </div>
            <div id="content">
                <div id="content_top">
                    尊敬的用户：您好！

                    您正在进行邮箱验证，请点击以下链接完成验证：
                    <div id="verificationCode">
                        <a href="{}"><button class="button">验证邮箱</button></a>
                    </div>
                    若不是您在操作，请忽略此邮件。
                    <div id="content_bottom">
                        <small>
                        如果您无法点击以上链接，请将此链接复制到浏览器地址栏中访问。
                        <a href="{}">{}</a>
                        </small>
                    </div>
                </div>
            </div>
            <div id="bottom">
                <div>
                    <p>此为系统邮件，请勿回复<br>
                    </p>
                    <p id="sign">—— OpenTeens 社区</p>
                </div>
            </div>
        </td>
    </tr>
    </tbody>
</table>
</body>
    """

    title = "OpenTeens 邮箱验证"
    from_ = "OpenTeens <noreply@openteens.org>"
    to = target
    content = template.format(uri, uri, uri)
    

