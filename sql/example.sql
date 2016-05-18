
INSERT INTO `Users`(`userId`, `userName`, `userType`) VALUES
('10000', 'admin', '0'),
('25000', 'TeacherChen', '1'),
('13307130000', 'Wan', '2'),
('13307130001', 'Chen', '2'),
('13307130002', 'Liang', '2')

INSERT INTO `Courses`(`courseId`, `courseName`, `teacherId`) VALUES
('100001', `软件工程`, `25000`)

INSERT INTO `Classes`(`studentId`, `courseId`) VALUES
('13307130000', '100001'),
('13307130001', '100001'),
('13307130002', '100001')

INSERT INTO `Assignments`(`assignmentId`, `courseId`, `assignmentName`, `description`, `addTime`, `deadlineTime`) VALUES
('10000101', `100001`, `Lab4`, `本次Lab需要实现系统的一个主要功能模块，并进行测试`, `2016-5-17 00:00:00`, `2016-5-30 23:59:59`)
