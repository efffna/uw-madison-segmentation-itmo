import path from 'path'
import express from 'express'
import multer from 'multer'
const router = express.Router()

const formatBytes = (bytes, decimals = 2) => {
	if (bytes === 0) return '0 Bytes'
	const k = 1024
	const dm = decimals < 0 ? 0 : decimals
	const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']

	const i = Math.floor(Math.log(bytes) / Math.log(k))
	return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i]
}

const storage = multer.diskStorage({
	destination(req, file, cb) {
		const uploadFolder = req.headers.folder
		cb(null, `uploads/${uploadFolder || ''}`)
	},
	filename(req, file, cb) {
		cb(
			null,
			`${
				file.originalname.split('.')[0]
			}-global-town-${Date.now()}${path.extname(file.originalname)}`
				.toLowerCase()
				.replace(/_/g, '-')
				.replace(' ', '-')
		)
	},
})

function checkFileType(file, cb) {
	const filetypes = /jpg|jpeg|png|svg+xml|svg|webp|pjpeg/
	const extname = filetypes.test(path.extname(file.originalname).toLowerCase())
	const mimetype = filetypes.test(file.mimetype)

	if (!extname && !mimetype) {
		return cb(new Error('Ты можешь загрузить только картинки!'), false)
	}

	return cb(null, true)
}

const upload = multer({
	storage,
	fileFilter: function (req, file, cb) {
		checkFileType(file, cb)
	},
}).array('imagesUp', 10)

router.post('/', (req, res) => {
	upload(req, res, function (err) {
		if (err) {
			console.log(err.message)

			res.status(400).json({
				status: 'Не удалось загрузить',
				message: err,
			})
		} else {
			const files = req.files
			if (!files) {
				res.status(400)
				throw new Error('Пожалуйста, загрузи файл')
			}

			let paths = []

			files.map((file, index) =>
				paths.push({
					_id: index,
					name: file.filename,
					path: `/${file.path}`,
					size: formatBytes(file.size),
				})
			)

			res.status(200).json({
				status: 'success',
				message: 'Файл успешно загружен',
				data: paths,
			})
		}
	})
})

export default router
