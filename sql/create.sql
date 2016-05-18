-- This SQL is for MySQL.
-- It may not run well in other databases.

create table if not exists `Users` (
    `userId` varchar(11) not NULL,
    `userName` varchar(30) not NULL,
    `userType` int not NULL,
    Primary Key(userId)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

create table if not exists `Courses` (
    `courseId` varchar(30) Primary Key,
    `courseName` varchar(30) not NULL,
    `teacherId` varchar(11),
    Primary Key(courseId),
    Foreign Key(teacherId) References Users(userId)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

create table if not exists `Classes` (
    `studentId` varchar(11) not NULL,
    `courseId` varchar(11) not NULL,
    Primary Key(studentId, teacherId),
    Foreign Key(studentId) References Users(userId),
    Foreign Key(courseId) References Courses(courseId)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

create table if not exists `Assignments` (
    `assignmentId` varchar(30) not NULL,
    `courseId` varchar(30) not NULL,
    `assignmentName` varchar(30) not NULL,
    `description` varchar(200),
    `addTime` datetime not NULL,
    `deadlineTime` datetime,
    Primary Key(assignmentId),
    Foreign Key(courseId) References Courses(courseId),
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

create table if not exists `Submissions` (
    `submissionId` varchar(30) not NULL,
    `assignmentId` varchar(30) not NULL,
    `studentId` varchar(11) not NULL,
    `content` varchar(500) not NULL,
    `submissionTime` datetime not NULL,
    `score` int,
    `comments` varchar(200),
    Primary Key(submissionId),
    Foreign Key(assignmentId) References Assignments(assignmentId),
    Foreign Key(studentId) References Users(userId),
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
