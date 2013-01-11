dir=/var/www/blog

all: ctagsfile  etagsfile filenametagsnew cscope
	echo "succus"

ctagsfile:
	ctags -R -o ctags ${dir}

etagsfile:
	ctags -e -o etags -R ${dir}

cscope:
	find ${dir} -type f -regex '.*\.\(py\|js\)' > cscope.files
	cscope -bq

filenametagsnew:
	echo -e "!_TAG_FILE_SORTED\t2\t2/2=foldcase/" > filenametags
	find ${dir} -not -regex '.*\.\(png\|gif\|jpg\)' -type f -printf "%f\t%p\t0\n" | sort -f >> filenametags

clean:
	rm -rf ctags etags cscope* filenametags
