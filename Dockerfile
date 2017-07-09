FROM fedora

MAINTAINER cbdavide <cbdavide@gmail.com>

RUN dnf -y update && dnf clean all
RUN dnf -y install python2 python2-mapnik pyqt4 && dnf clean all

WORKDIR /usr/app

COPY . .

CMD ["python", "src/visor/VisorShapefiles.py"]
