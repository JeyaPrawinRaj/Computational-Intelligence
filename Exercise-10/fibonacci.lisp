(defun fib2(n)
  (cond
    ((= n 0) 0)
    ((= n 1) 1)
    (t (+ (fib2 (- n 1)) (fib2 (- n 2))))
  )
)
