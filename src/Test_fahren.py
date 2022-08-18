import evimport ev3dev.ev3 as ev3
import time

m_l = ev3.LargeMotor("outA")
m_r = ev3.LargeMotor("outC")
m_l.reset()
m_r.reset()

m_l.stop_action = "brake"
m_r.stop_action = "brake"

m_l.speed_sp = 100
m_r.speed_sp = 100

m_l.command = "run-forever"
m_r.command = "run-forever"

time.sleep(3)

m_l.speed_sp = 100
m_r.speed_sp = -100

m_r.command = "run-forever"
m_l.command = "run-forever"

time.sleep(3)
m_l.stop()
m_r.stop()