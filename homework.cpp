#include "homework.h"
#include "ui_homework.h"

homework::homework(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::homework)
{
    ui->setupUi(this);
}

homework::~homework()
{
    delete ui;
}

void homework::on_spinbox_interval_valueChanged(double arg1)
{

}
