echo "Roll 2 sets of 5x(2d6+6) and choose one to use:"
echo "__Set 1__"
for i in {0..5}; do python roll.py 2d6+6; done
echo "__Set 2__"
for i in {0..5}; do python roll.py 2d6+6; done
