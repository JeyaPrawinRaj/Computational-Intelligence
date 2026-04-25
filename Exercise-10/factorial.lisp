(defun fact2(n)
  (if (= n 0)
      1
      (* n (fact2 (- n 1)))
  )
)
