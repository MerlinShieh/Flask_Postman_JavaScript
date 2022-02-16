
# flask 文件上传配置
flask_config = {
	"__UPLOAD_FOLDER": r'./files/uploads',
	"__ALLOWED_EXTENSIONS": {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'},
	"__MAX_CONTENT_LENGTH": 16 * 1024 * 1024  # 16MB
}