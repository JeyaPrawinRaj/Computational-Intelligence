(defun palin(str)
  (equal str (coerce (reverse (coerce str 'list)) 'string))
)
