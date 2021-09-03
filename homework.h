#ifndef HOMEWORK_H
#define HOMEWORK_H

#include <QMainWindow>

namespace Ui {
class homework;
}

class homework : public QMainWindow
{
    Q_OBJECT

public:
    explicit homework(QWidget *parent = nullptr);
    ~homework();

private slots:
    void on_combobox_interval_activated(const QString &arg1);

    void on_spinbox_interval_valueChanged(double arg1);

private:
    Ui::homework *ui;
};

#endif // HOMEWORK_H
